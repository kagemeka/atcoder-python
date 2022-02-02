from __future__ import annotations

import logging
import types
import typing

import requests

from atcoder.core.auth import (
    InvalidSessionError,
    LoginCredentials,
    is_logged_in,
)
from atcoder.core.crawl.submission_results import SubmissionsSearchParams
from atcoder.core.language import Language
from atcoder.core.submission_result import SubmissionResult
from atcoder.login import login
from atcoder.submission_result import fetch_all_my_submission_results
from atcoder.submit import fetch_languages, submit_task

logger = logging.getLogger(__name__)


class UserSessionAgent:
    __credentials: LoginCredentials
    __session: typing.Optional[requests.Session] = None

    def __init__(
        self,
        credentials: LoginCredentials,
    ) -> None:
        self.__credentials = credentials

    def __enter__(self) -> UserSessionAgent:
        return self

    def __exit__(
        self,
        __exc_type: typing.Optional[type[BaseException]] = None,
        __exc_val: typing.Optional[BaseException] = None,
        __exc_tb: typing.Optional[types.TracebackType] = None,
    ) -> None:
        if self.__session is not None:
            self.__session.close()

    async def __update_session(self) -> None:
        if self.__session is None or not is_logged_in(self.__session):
            try:
                self.__session = await login(self.__credentials)
            except InvalidSessionError as exception:
                logger.error(str(exception))
                raise exception

    async def submit(
        self,
        contest_id: str,
        task_id: str,
        source_code: str,
        language_id: int,
    ) -> None:
        await self.__update_session()
        assert self.__session is not None
        await submit_task(
            self.__session,
            contest_id,
            task_id,
            source_code,
            language_id,
        )

    async def fetch_languages(self) -> typing.List[Language]:
        await self.__update_session()
        assert self.__session is not None
        return await fetch_languages(self.__session)

    async def fetch_my_submissions(
        self,
        contest_id: str,
        params: typing.Optional[SubmissionsSearchParams] = None,
    ) -> typing.AsyncIterator[typing.List[SubmissionResult]]:
        await self.__update_session()
        assert self.__session is not None
        async for submissions in fetch_all_my_submission_results(
            self.__session,
            contest_id,
            params,
        ):
            yield submissions
