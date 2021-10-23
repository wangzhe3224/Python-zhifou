#!/usr/bin/env python
import subprocess
import click
import time
from multiprocessing import Pool


SECOND = float
IO = None

def cut_points(total_length, target_length: SECOND):
    l = total_length
    cuts = int(l / target_length)
    res = []
    for i in range(cuts):
        res.append((i*target_length, target_length))
    res.append(((i+1)*target_length, target_length))

    return res


def get_length(filename) -> SECOND:
    # in seconds
    result = subprocess.run(["ffprobe", "-v", "error", "-show_entries",
                             "format=duration", "-of",
                             "default=noprint_wrappers=1:nokey=1", filename],
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT
        )
    return float(result.stdout)


def cut_video(source: str, start: int, end: int, target_path: str) -> IO:
    # note: overwrite existed files.
    result = subprocess.run(["ffmpeg", "-ss", f"{start}",
                             "-i", f"{source}",
                             "-to", f"{end}", "-c", "copy", target_path],
                            input="y",
                            capture_output=True,
                            text=True
                            )


def to_time_str(seconds: float):
    return time.strftime('%H:%M:%S', time.gmtime(seconds))


def gen_params(source: str, target_forder: str = '.', target_name: str = None,
               target_length: int = 300):
    
    total = get_length(source)
    sectors = cut_points(total_length=total, target_length=target_length)

    print(f"Preview: \n{source} \nTotal length: {total} \nTarget path: {target_forder}\nTarget section length {target_length} \nSections: {sectors}")
    
    if target_name is None:
        target_name = source.split('/')[-1]

    filename, extension = target_name.split('.')

    params = []

    for idx, sector in enumerate(sectors):
        start, end = sector
        target_path = f"{target_forder}/{filename}_{idx}.{extension}"

        params.append((
            source,
            to_time_str(start),
            to_time_str(end),
            target_path
        ))

    return params


@click.command()
@click.argument('source')
@click.option('-t', '--target-folder', default='.', help="target folder of the outputs")
@click.option('-n', '--target-name', default=None, help="target file name of the outputs")
@click.option('-l', '--target-length',  default=300, help="target file length")
@click.option('-w', '--worker', default=8)
def main(source: str, target_folder: str = '.', target_name: str = None,
         target_length: int = 300, worker: int=8):

    params = gen_params(source, target_folder, target_name, target_length)

    with Pool(worker) as p:
        p.starmap(cut_video, params)


if __name__ == '__main__':
    
    main()
