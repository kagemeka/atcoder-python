from __future__ import annotations

import logging
import types
import typing

import requests

import atcoder.auth
import atcoder.language
import atcoder.login
import atcoder.submission
import atcoder.submit

_LOGGER = logging.getLogger(__name__)


class UserSessionAgent:
    __credentials: atcoder.auth.LoginCredentials
    __session: typing.Optional[requests.Session] = None

    def __init__(
        self,
        credentials: atcoder.auth.LoginCredentials,
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

    def __update_session(self) -> None:
        if self.__session is None or not atcoder.auth._is_logged_in(
            self.__session
        ):
            try:
                self.__session = atcoder.login.login(self.__credentials)
            except atcoder.auth.InvalidSessionError as exception:
                _LOGGER.error(str(exception))
                raise exception

    def submit(
        self,
        contest_id: str,
        task_id: str,
        source_code: str,
        language_id: int,
    ) -> None:
        self.__update_session()
        assert self.__session is not None
        atcoder.submit.submit_task(
            self.__session,
            contest_id,
            task_id,
            source_code,
            language_id,
        )

    def fetch_languages(self) -> typing.List[atcoder.language.Language]:
        self.__update_session()
        assert self.__session is not None
        return atcoder.submit.fetch_languages(self.__session)

    def fetch_my_submissions(
        self,
        contest_id: str,
        params: typing.Optional[
            atcoder.submission.SubmissionsSearchParams
        ] = None,
    ) -> typing.Iterator[atcoder.submission.SubmissionResult]:
        self.__update_session()
        assert self.__session is not None
        yield from atcoder.submission.fetch_all_my_submission_results(
            self.__session,
            contest_id,
            params,
        )
