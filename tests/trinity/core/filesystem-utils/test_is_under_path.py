import pytest

from trinity.utils.filesystem import (is_under_path,)


@pytest.mark.parametrize(
    'base_path,path,expected',
    (('foo', 'foo', False), ('foo', 'foo/bar/..', False), ('foo', '..', False), ('foo', 'foo/bar/../../', False), ('foo', '/foo/bar', False), ('foo', '/foo', False), ('foo', 'foo/bar.sol', True), ('foo', 'foo/bar', True), ('foo', 'foo/bar/../../foo/baz', True)),
    # Same Path
    # up a directory (or two)
    # relative and abs
    # actually nested
)
def test_is_under_path(base_path, path, expected):
    actual = is_under_path(base_path, path)
    assert actual is expected


@pytest.mark.parametrize(
    'base_path,path,expected',
    (('foo', 'foo', True), ('foo', 'foo/bar/..', True), ('foo', '..', False), ('foo', 'foo/bar/../../', False), ('foo', '/foo/bar', False), ('foo', '/foo', False), ('foo', 'foo/bar.sol', True), ('foo', 'foo/bar', True), ('foo', 'foo/bar/../../foo/baz', True)),
    # Same Path
    # up a directory (or two)
    # relative and abs
    # actually nested
)
def test_is_under_path_not_strict(base_path, path, expected):
    actual = is_under_path(base_path, path, strict=False)
    assert actual is expected
