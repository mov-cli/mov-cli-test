from __future__ import annotations
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from typing import Iterable, Optional, Dict

    from mov_cli import Config
    from mov_cli.http_client import HTTPClient
    from mov_cli.scraper import ScraperOptionsT

from pytubefix import YouTube
from devgoldyutils import Colours

from mov_cli.utils import EpisodeSelector
from mov_cli import Scraper, Multi, Single, Metadata, MetadataType

__all__ = ("TestScraper",)

class TestScraper(Scraper):
    def __init__(self, config: Config, http_client: HTTPClient, options: Optional[ScraperOptionsT] = None) -> None:
        self.creative_common_films = [
            Metadata(id = "https://youtu.be/aqz-KE-bpKQ", title = "Big Buck Bunny", type = MetadataType.SINGLE, year = "2008"),
            Metadata(id = "https://www.youtube.com/watch?v=BBgghnQF6E4", title = "Steamboat Willie", type = MetadataType.SINGLE, year = "1928"),
            Metadata(id = "https://cdn.devgoldy.xyz/ricky.webm", title = "Ricky :)", type = MetadataType.SINGLE, year = "2009"),
            Metadata(id = "https://youtu.be/u9lj-c29dxI", title = "Wing It!", type = MetadataType.SINGLE, year = "2023"),
            Metadata(id = "https://youtu.be/UXqq0ZvbOnk", title = "Charge", type = MetadataType.SINGLE, year = "2022"),
            Metadata(id = "https://youtu.be/_cMxraX_5RE", title = "Sprite Fright", type = MetadataType.SINGLE, year = "2021"),
            Metadata(id = "https://youtu.be/WhWc3b3KhnY", title = "Spring", type = MetadataType.SINGLE, year = "2019"),
        ]

        self.message = f"""
  ✨ {Colours.CLAY}Welcome to {Colours.PURPLE}mov-cli{Colours.RESET}!!!

  mov-cli is a command line tool used to stream or watch anything and everything from the comfort of your terminal.
  The plugin you just executed right now is a test plugin that contains some free films and animations in the creative commons.

  {Colours.BLUE}To leverage the full power of mov-cli you must install more plugins.{Colours.RESET}

  You can find third-party plugins over here: {Colours.PINK_GREY}https://github.com/topics/mov-cli-plugin{Colours.RESET}
  Then you can find the instructions on how to install a plugin over here: {Colours.PINK_GREY}https://github.com/mov-cli/mov-cli/wiki/Plugins{Colours.RESET}
        """

        super().__init__(config, http_client, options)

    def search(self, query: str, limit: int = None) -> Iterable[Metadata]:
        # This is where you would want to implement searching for your scraper. 
        # This method is called whenever the user searches for something.

        # ignore this
        # -------------
        if query.lower() in ["abc", "all", "example", "query"]:
            self.logger.warning("This is an example/test plugin for mov-cli, press enter to skip if you aren't new to that.")
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

    def scrape(self, metadata: Metadata, episode: EpisodeSelector) -> Multi | Single:
        scrape_stream_url = self.options.get("use_stream_url", False)

        url = metadata.id

        if scrape_stream_url is True and "https://youtu.be" in url:
            url = YouTube(url).streams.get_highest_resolution().url

        # NOTE: I could have just dropped multi as all the media in my list are 
        # films and not series but I'll leave it in here as an example.
        if metadata.type == MetadataType.MULTI:
            return Multi(
                url = url, 
                title = metadata.title, 
                referrer = url, 
                episode = episode, 
                subtitles = None
            )

        return Single(
            url = url, 
            title = metadata.title, 
            referrer = url, 
            year = metadata.year
        )

    def scrape_episodes(self, metadata: Metadata) -> Dict[int | None, int]:
        # NOTE: Let's just return None for now as we don't have any series in the list hence no episodes.
        return {None: 1}