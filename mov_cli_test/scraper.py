from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Optional, Dict

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient

from pytube import YouTube
from devgoldyutils import Colours, LoggerAdapter

from mov_cli.logger import mov_cli_logger
from mov_cli.utils import EpisodeSelector
from mov_cli import Scraper, Series, Movie, Metadata, MetadataType

__all__ = ("TestScraper",)

logger = LoggerAdapter(mov_cli_logger, prefix = "Test")

class TestScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient) -> None:
        self.creative_common_films = [
            Metadata(id = "https://youtu.be/aqz-KE-bpKQ", title = "Big Buck Bunny", type = MetadataType.MOVIE, year = "2008"),
            Metadata(id = "https://www.youtube.com/watch?v=BBgghnQF6E4", title = "Steamboat Willie", type = MetadataType.MOVIE, year = "1928"),
            Metadata(id = "https://cdn.devgoldy.xyz/ricky.webm", title = "Ricky :)", type = MetadataType.MOVIE, year = "2009")
        ]

        self.message = f"""
  ✨ {Colours.CLAY}Welcome to {Colours.PURPLE}mov-cli{Colours.RESET}!!!

  mov-cli is a command line tool used to stream or watch anything and everything from the comfort of your terminal.
  The plugin you just executed right now is a test plugin that contains some free films and animations in the creative commons.

  {Colours.BLUE}To leverage the full power of mov-cli you must install more plugins.{Colours.RESET}

  You can find third-party plugins over here: {Colours.PINK_GREY}https://github.com/topics/mov-cli-plugin{Colours.RESET}
  Then you can find the instructions on how to install a plugin over here: {Colours.PINK_GREY}https://github.com/mov-cli/mov-cli/wiki/Plugins{Colours.RESET}
        """

        super().__init__(config, http_client)

    def search(self, query: str, limit: int = None) -> Iterable[Metadata]:
        # This is where you would want to implement searching for your scraper. 
        # This method is called whenever the user searches for something.

        # ignore this
        # -------------
        if query.lower() in ["abc", "all", "example"]:
            logger.warning("This is an example/test plugin for mov-cli, press enter to skip if you aren't new to that.")
            input(self.message + Colours.GREEN.apply("\n  Press ENTER to continue... "))
            for x in self.creative_common_films: yield x

        # There's two ways of doing this, I highly encourage the second but here's the first way.
        """
        search_results: List[Metadata] = []

        for metadata in self.creative_common_films:

            if query in metadata.title:
                search_results.append(metadata)

        return search_results
        """

        # Then here's the second and better way.
        for metadata in self.creative_common_films:

            # this is basically a poor mans search algorithm.
            if query.lower() in metadata.title.lower():
                yield metadata # yield the element instead of appending it to a list for better performance and UX.

    def scrape(self, metadata: Metadata, episode: Optional[EpisodeSelector] = None, **kwargs) -> Series | Movie:
        if episode is None:
            episode = EpisodeSelector()

        url = metadata.id

        if "https://youtu.be" in url:
            url = YouTube(url).streams.get_highest_resolution().url

        # NOTE: I could have just dropped series as all the media in my list are 
        # films and not series but I'll leave it in here as an example.
        if metadata.type == MetadataType.SERIES:
            return Series(
                url = url, 
                title = metadata.title, 
                referrer = url, 
                episode = episode, 
                subtitles = None
            )

        return Movie(
            url = url, 
            title = metadata.title, 
            referrer = url, 
            year = metadata.year,
            subtitles = None
        )

    def scrape_episodes(self, metadata: Metadata, **kwargs) -> Dict[int | None, int]:
        # NOTE: Let's just return None for now as we don't have any series in the list hence no episodes.
        return {None: 1}