# Run with pytest -s -v
import random
import string
from dataclasses import dataclass
from enum import Enum

import pytest


class Direction(Enum):
    REQUEST = 'request'
    RESPONSE = 'response'


class Location(Enum):
    BODY = 'body'
    HEADER = 'header'
    QUERY = 'query'


class Method(Enum):
    GET = 'get'
    POST = 'post'
    PUT = 'put'
    DELETE = 'delete'
    PATCH = 'patch'


class SpecState(Enum):
    APPROVED = 'approved'
    DIFF = 'diff'
    DIFF_REQUIRED = 'diff_required'
    DIFF_SENSITIVE = 'diff_sensitive'
    DIFF_REQUIRED_SENSITIVE = 'diff_required_sensitive'


@pytest.fixture
def unique_id():
    return ''.join(random.sample(string.ascii_letters + string.digits, 10))


@pytest.fixture(params=Direction)
def direction(request):
    return request.param


@pytest.fixture(params=Location)
def location(request):
    return request.param


@pytest.fixture(params=Method)
def method(request):
    return request.param


@pytest.fixture(params=SpecState)
def spec_state(request):
    return request.param


@dataclass
class Options:
    unique_id: str
    direction: Direction
    location: Location
    method: Method
    spec_state: SpecState


def create_spec(options: Options):
    result = {"openapi": "3.0.0", "paths": {}}

    result["paths"][f"/{options.unique_id}/hello"] = {options.method.value: {}}

    return result


def create_schema(options: Options):
    pass


def test_api(unique_id, direction, location, method, spec_state):
    options = Options(unique_id, direction, location, method, spec_state)

    spec = create_spec(options)
    schema = create_schema(options)

    print(f'Running test on spec: {spec!r}')
