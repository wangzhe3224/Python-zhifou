from __future__ import annotations
import typing as tp
from typing import Generator, List, Any, Optional, Sequence
from abc import ABC, abstractmethod, abstractproperty

# --- Interface and Abstract classes --- #

class Media(ABC):

    @abstractproperty
    def name(self) -> str:
        ...

    @abstractproperty
    def description(self) -> str:
        ...

    @abstractproperty
    def totalRunningMins(self) -> int:
        ...

    @abstractmethod
    def accept(self, visitor: Visitor):
        ...

    def __str__(self) -> str:
        return f"{str(self.__class__).split('.')[-1][:-2]} - {self.name} - {self.description} - {self.totalRunningMins} min"

    def __repr__(self) -> str:
        return self.__str__()


class StandloneMedia(Media):

    def __init__(self, name: str, des: str, run: int) -> None:
        self._name: str = name
        self._description: str = des
        self._run: int = run

    def accept(self, visitor: Visitor):
        visitor.visitMedia(self)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def totalRunningMins(self) -> int:
        return self._run


class Series(Media):

    def __init__(self, name: str, des: str, children: Sequence[Media]) -> None:
        self._name: str = name
        self._description: str = des
        self._children = children

    def accept(self, visitor: Visitor):
        for child in self._children:
            child.accept(visitor)

    @property
    def name(self) -> str:
        return self._name

    @property
    def description(self) -> str:
        return self._description

    @property
    def totalRunningMins(self) -> int:
        _sum = 0
        for media in self._children:
            _sum += media.totalRunningMins

        return _sum


class MediaInfoDecoration(Media):

    def __init__(self, media: Media) -> None:
        self._media = media

    @property
    def name(self) -> str:
        return self._media.name

    @property
    def description(self) -> str:
        return self._media.description

    @property
    def totalRunningMins(self) -> int:
        return self._media.totalRunningMins

    def accept(self, visitor: Visitor):
        return self._media.accept(visitor)


class Visitor(ABC):

    @abstractmethod
    def visitMedia(self, midia: Media) -> Any:
        ...


class Query(ABC):
    
    def __init__(self, medias: Sequence[Media], queryStrategy: QueryStrategy) -> None:
        self._medias = medias
        self._strategy = queryStrategy
        self._strategy.plugMedia(medias)
    
    @abstractmethod
    def query(self) -> Sequence[Optional[Media]]:
        ...


class QueryStrategy(ABC):

    @abstractmethod
    def plugMedia(self, medias: Sequence[Media]):
        ...
    
    @abstractmethod
    def next(self) -> Optional[Media]:
        ...

# --- concrete classes --- #
# --- Media --- #


class Episode(StandloneMedia):

    def __init__(self, name: str, des: str, run: int) -> None:
        super().__init__(name, des, run)


class Film(StandloneMedia):

    def __init__(self, name: str, des: str, run: int) -> None:
        super().__init__(name, des, run)


class TVSeries(Series):

    def __init__(self, name: str, des: str, children: Sequence[Episode]) -> None:
        super().__init__(name, des, children)

    def __str__(self) -> str:
        return f"{str(self.__class__).split('.')[-1][:-2]} - {self.name} - {self.description} - {self.totalRunningMins} min - {len(self._children)} eqisodes"


class FilmSeries(Series):

    def __init__(self, name: str, des: str, children: Sequence[Film]) -> None:
        super().__init__(name, des, children)

    def __str__(self) -> str:
        return f"{str(self.__class__).split('.')[-1][:-2]} - {self.name} - {self.description} - {self.totalRunningMins} min - {len(self._children)} films"

# --- Decorator --- #


class TextDecorator(MediaInfoDecoration):

    def text(self):
        # TODO: handle series and single differently
        return f"Text: {self._media.name} - {self._media.description}"


class ImageDecorator(MediaInfoDecoration):

    def image(self):
        # TODO: handle series and single differently
        return f"Image: http://{self._media.name}-{self._media.description}.png"

# --- Visitor --- #


class HTMLVisitor(Visitor):

    def visitMedia(self, media: Media):
        textDec: TextDecorator = TextDecorator(media=media)
        imageDec: ImageDecorator = ImageDecorator(media=media)
        text = textDec.text()
        image = imageDec.image()
        print(f"{text}\n{image}")


# --- Application --- #
class MediaApplication:

    def __init__(self) -> None:
        self._medias: List[Optional[Media]] = []

    def add(self, media: Media):
        self._medias.append(media)

    def show_media(self):
        for media in self._medias:
            print(media)

# --- Strategy --- #
class LinearQuery(Query):

    def __init__(self, medias: Sequence[Media], queryStrategy: QueryStrategy) -> None:
        super().__init__(medias, queryStrategy)
    
    def query(self) -> Sequence[Optional[Media]]:
        res: List[Optional[Media]] = []        
        _next = self._strategy.next()
        while _next:
            res.append(_next)
            _next = self._strategy.next()

        return res


class FilmFilter(QueryStrategy):
    
    def __init__(self) -> None:
        self._medias: Sequence[Media] = []
        self._counter: int = 0
    
    def next(self) -> Optional[Media]:
        while self._counter < len(self._medias):
            res: Media = self._medias[self._counter]
            if isinstance(res, Film):
                self._counter += 1
                return res
            else:
                self._counter += 1

        return None 


class LongMedia(QueryStrategy):
    
    def __init__(self, limit: int) -> None:
        self._medias: Sequence[Media] = []
        self._counter: int = 0
        self._limit = limit

    def plugMedia(self, medias: Sequence[Media]):
        self._medias = medias
    
    def next(self) -> Optional[Media]:
        while self._counter < len(self._medias):
            res: Media = self._medias[self._counter]
            if res.totalRunningMins > self._limit:
                self._counter += 1
                return res
            else:
                self._counter += 1

        return None        


if __name__ == '__main__':

    # Sample code
    print(f"----- Creating sample data objects: ")
    episodes1: List[Episode] = [
        Episode(f"episode x - {i}", "episodes x", 25) for i in range(30)]
    films: List[Film] = [
        Film(f"film x - {i}", "film x", 90) for i in range(10)]
    tvSeries1: Media = TVSeries(
        "episode x", "expisode x series decription", episodes1)
    filmSeries1: Media = FilmSeries(
        "film series x", "films x series decription", films)
    e1: Media = Episode('Single Episode x', 'Single Episode x Description', 50)
    f2: Media = Film('Single Film y', 'Single Film y Description', 120)

    print(f"\n-----  Show application code sample: ")
    app: MediaApplication = MediaApplication()
    app.add(e1)
    app.add(f2)
    app.add(tvSeries1)
    app.add(filmSeries1)
    app.show_media()
    print()

    print(f"-----  Show decorator and visitor sample code: ")
    visitor = HTMLVisitor()
    medias: List[Media] = [e1, f2, tvSeries1, filmSeries1]
    for media in medias:
        media.accept(visitor)
    print()

    print(f"-----  Show query strategy sample code: ")
    longFilter: LongMedia = LongMedia(100)
    query: Query = LinearQuery(medias=medias, queryStrategy=longFilter)
    print(query.query())
