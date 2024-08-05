import json
from typing import Dict, Literal, Optional, Any, Union, List

import aiohttp
import aiofiles

class Jiosaavn:
    """
    A class to interact with the JioSaavn API for searching and downloading songs, albums, artists, and playlists.
    """

    BASE_URL = "https://www.jiosaavn.com"
    API_URL = f"{BASE_URL}/api.php"

    async def _request_data(
        self,
        url: str,
        params: Dict[str, Any]
    ) -> Union[Dict[str, Any], List[Any]]:
        """
        Makes an asynchronous GET request to the specified URL with the given parameters.

        Args:
            url (str): The URL to send the GET request to.
            params (Dict[str, Any]): The query parameters for the GET request.

        Returns:
            Union[Dict[str, Any], List[Any]]: The JSON response from the request.

        Raises:
            RuntimeError: If there is an error during the request or if the response cannot be decoded as JSON.
        """
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(url=url, params=params) as response:
                    response.raise_for_status()  # Raise an exception for HTTP errors
                    response_text = await response.text()
                    return json.loads(response_text)
        except aiohttp.ClientError as e:
            raise RuntimeError(f"Request to {url} failed: {e}")
        except ValueError as e:
            raise RuntimeError(f"Failed to decode JSON response from {url}: {e}")

    async def search(
        self,
        query: str,
        search_type: Literal["songs", "albums", "artists", "playlists"],
        page_no: Optional[int] = 1,
        page_size: Optional[int] = 10
    ) -> Dict[str, Any]:
        """
        Search for songs, albums, artists, or playlists.

        Args:
            query (str): The search query string.
            search_type (Literal["songs", "albums", "artists", "playlists"]): The type of search to perform.
            page_no (Optional[int]): The page number for paginated results. Defaults to 1.
            page_size (Optional[int]): The number of results per page. Defaults to 10.

        Returns:
            Dict[str, Any]: The search results from the API.

        Raises:
            ValueError: If `page_no` or `page_size` are not positive integers, or if `search_type` is invalid.
        """
        if page_no is not None and page_no < 1:
            raise ValueError("`page_no` must be a positive integer.")
        if page_size is not None and page_size < 1:
            raise ValueError("`page_size` must be a positive integer.")

        search_type_call_map = {
            "songs": "search.getResults",
            "albums": "search.getAlbumResults",
            "artists": "search.getArtistResults",
            "playlists": "search.getPlaylistResults",
        }

        call = search_type_call_map.get(search_type)
        if not call:
            raise ValueError(f"Invalid search_type: {search_type}")

        params = {
            'p': page_no,
            'q': query,
            '__call': call,
            'api_version': 4,
            'n': page_size,
            '_format': 'json',
            '_marker': 0,
            'ctx': 'web6dot0'
        }

        return await self._request_data(self.API_URL, params=params)

    async def search_all_types(
        self,
        query: str
    ) -> Dict[str, Any]:
        """
        Retrieve search results across all types, returning a limited subset due to API constraints.

        Args:
            query (str): The search query string.

        Returns:
            Dict[str, Any]: The search results from the API.
        """
        params = {
            '_format': 'json',
            '_marker': 0,
            'query': query,
            '__call': 'autocomplete.get',
            'ctx': 'web6dot0'
        }
        return await self._request_data(self.API_URL, params=params)

    async def get_artist(
        self,
        artist_id: Optional[str] = None,
        page_no: Optional[int] = 1,
        page_size: Optional[int] = 10
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the details of an artist based on the provided ID.

        Args:
            artist_id (Optional[str]): The unique identifier for the artist. Defaults to None.
            page_no (Optional[int]): The page number for paginated results. Defaults to 1.
            page_size (Optional[int]): The number of results per page. Defaults to 10.

        Returns:
            Optional[Dict[str, Any]]: The details from the API or None if no response.

        Raises:
            ValueError: If `page_no` or `page_size` are not positive integers.
        """
        if page_no < 1:
            raise ValueError("`page_no` must be a positive integer.")
        if page_size < 1:
            raise ValueError("`page_size` must be a positive integer.")

        params = {
            '__call': 'webapi.get',
            'token': artist_id,
            'type': "artist",
            'p': page_no,
            'n_song': page_size,
            'n_album': page_size,
            'includeMetaTags': 0,
            'ctx': 'web6dot0',
            'api_version': 4,
            '_format': 'json',
            '_marker': 0
        }

        response = await self._request_data(self.API_URL, params=params)
        if not response:
            return None

        start_index = (page_no - 1) * page_size
        end_index = page_no * page_size
        response["topSongs"] += response["topAlbums"]
        response['count'] = len(response["topSongs"])
        response['topSongs'] = response["topSongs"][start_index:end_index]
        return response

    async def get_playlist_or_album(
        self,
        album_id: Optional[str] = None,
        playlist_id: Optional[str] = None,
        page_no: Optional[int] = 1,
        page_size: Optional[int] = 10
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the details of a playlist or album based on the provided ID.

        Args:
            album_id (Optional[str]): The unique identifier for the album. Defaults to None.
            playlist_id (Optional[str]): The unique identifier for the playlist. Defaults to None.
            page_no (Optional[int]): The page number for paginated results. Defaults to 1.
            page_size (Optional[int]): The number of results per page. Defaults to 10.

        Returns:
            Optional[Dict[str, Any]]: The details from the API or None if no response or empty list for albums.

        Raises:
            ValueError: If both `album_id` and `playlist_id` are None or if `page_no` or `page_size` are not positive integers.
        """
        if page_no < 1:
            raise ValueError("`page_no` must be a positive integer.")
        if page_size < 1:
            raise ValueError("`page_size` must be a positive integer.")
        if not album_id and not playlist_id:
            raise ValueError("Either `album_id` or `playlist_id` must be provided.")

        search_type = "album" if album_id else "playlist"
        token = album_id or playlist_id

        params = {
            '__call': 'webapi.get',
            'token': token,
            'type': search_type,
            'p': page_no,
            'n': page_size,
            'includeMetaTags': 0,
            'ctx': 'web6dot0',
            'api_version': 4,
            '_format': 'json',
            '_marker': 0
        }

        response = await self._request_data(self.API_URL, params=params)
        if not response:
            return None

        if search_type == "playlist":
            return response

        if not response.get("list"):
            return None

        start_index = (page_no - 1) * page_size
        end_index = page_no * page_size
        response['list'] = response["list"][start_index:end_index]
        more_info = response.get("more_info", {})
        album_url = more_info.get("album_url")

        if not album_url:
            return response

        response["perma_url"] = album_url
        return response

    async def get_song(
        self,
        song_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves the details of a song based on the song ID.

        Args:
            song_id (str): The unique identifier for the song.

        Returns:
            Dict[str, Any]: The song details from the API.
        """
        params = {
            '__call': 'webapi.get',
            'token': song_id,
            'type': 'song',
            'includeMetaTags': 0,
            'ctx': 'web6dot0',
            'api_version': 4,
            '_format': 'json',
            '_marker': 0
        }
        return await self._request_data(self.API_URL, params=params)

    async def get_song_lyrics(
        self,
        lyrics_id: str
    ) -> Dict[str, Any]:
        """
        Retrieves the lyrics of a song based on the lyrics ID.

        Args:
            lyrics_id (str): The ID of the lyrics to retrieve.

        Returns:
            Dict[str, Any]: The lyrics details from the API.

        Raises:
            ValueError: If the lyrics ID is invalid or the lyrics could not be retrieved.
        """
        params = {
            '__call': 'lyrics.getLyrics',
            'lyrics_id': lyrics_id,
            'type': 'song',
            'includeMetaTags': 0,
            'ctx': 'web6dot0',
            'api_version': 4,
            '_format': 'json',
            '_marker': 0
        }
        try:
            response = await self._request_data(self.API_URL, params=params)
            if not response:
                raise ValueError("No response received from the API.")
            return response
        except Exception as e:
            raise ValueError(f"Failed to retrieve lyrics for ID {lyrics_id}: {e}")

    async def get_download_url(
        self,
        song_id: str,
        bitrate: Literal[160, 320]
    ) -> Optional[Dict[str, Any]]:
        """
        Retrieves the download URL for a song based on the song ID and bitrate.

        Args:
            song_id (str): The unique identifier for the song.
            bitrate (Literal[160, 320]): The desired bitrate for the download.

        Returns:
            Optional[Dict[str, Any]]: The download data containing the URL or None if not found.
        """
        song_response = await self.get_song(song_id=song_id)
        if song_response:
            encrypted_media_url = song_response.get("songs", [])[0].get("more_info", {}).get("encrypted_media_url")
            params = {
                "__call": 'song.generateAuthToken',
                "url": encrypted_media_url,
                "bitrate": bitrate,
                "api_version": 4,
                "_format": "json",
                "ctx": "wap6dot0",
                "_marker": 0
            }
            return await self._request_data(url=self.API_URL, params=params)
        return None

    async def download_song(
        self,
        song_id: str,
        bitrate: Literal[160, 320],
        download_location: str
    ) -> None:
        """
        Downloads a song based on the song ID and bitrate.

        Args:
            song_id (str): The unique identifier for the song.
            bitrate (Literal[160, 320]): The desired bitrate for the download.
            download_location (str): The file path where the song will be saved.

        Raises:
            ValueError: If the song download URL cannot be retrieved.
        """
        download_data = await self.get_download_url(song_id=song_id, bitrate=bitrate)
        if not download_data or not download_data.get("auth_url"):
            raise ValueError("Unable to retrieve the download URL for the song.")

        url = download_data["auth_url"]

        async with aiohttp.ClientSession() as session:
            async with session.get(url) as response:
                response.raise_for_status()
                async with aiofiles.open(download_location, "wb") as file:
                    while True:
                        chunk = await response.content.read(4 * 1024 * 1024)  # 4 MB chunk size
                        if not chunk:
                            break
                        await file.write(chunk)
