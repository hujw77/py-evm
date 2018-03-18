import pytest

from evm.exceptions import (ValidationError,)

from evm.rlp.headers import (CollationHeader,)


@pytest.mark.parametrize(
    'header_bytes, expected_header_dict',
    (
        (
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xbd&\xfb\x06L\x1c\x85\xc9\x14\xad%\xfb\xbc\xfc\xef\xc5\x8bW\xe7\xaaJ\x91N\x9cj\xd0\x19n\xd7\xe1u\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00tx_list tx_list tx_list tx_list \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdfpost_stapost_stapost_stapost_stareceipt receipt receipt receipt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01',  # noqa: E501
            {
                'shard_id': 0,
                'expected_period_number': 5,
                'period_start_prevhash': b'\xbd&\xfb\x06L\x1c\x85\xc9\x14\xad%\xfb\xbc\xfc\xef\xc5\x8bW\xe7\xaaJ\x91N\x9cj\xd0\x19n\xd7\xe1u\xc6',
                'parent_hash': b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00',
                'transaction_root': b'tx_list tx_list tx_list tx_list ',
                'coinbase': b'~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdf',
                'state_root': b'post_stapost_stapost_stapost_sta',
                'receipt_root': b'receipt receipt receipt receipt ',
                'number': 1,
            },  # noqa: E501
        ),
        (
            b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\xd0x\t\x1a\xc1\xff!l\x19@\xd0T\x0fX\xd3!Ny\x89\xc3\x1dg\xa36\x11\xd5\x00j\x92\xb5\xd5\xeb\xd3\xf5\x00Y\xc7d\x82\xa4\x12\x16\xf3i=R\x1dS=j_N\xe9\xea\xb44`{pC\xacG\xcb\x9atx_list tx_list tx_list tx_list \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdfpost_stapost_stapost_stapost_stareceipt receipt receipt receipt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02',  # noqa: E501
            {
                'shard_id': 0,
                'expected_period_number': 6,
                'period_start_prevhash': b'\xd0x\t\x1a\xc1\xff!l\x19@\xd0T\x0fX\xd3!Ny\x89\xc3\x1dg\xa36\x11\xd5\x00j\x92\xb5\xd5\xeb',
                'parent_hash': b'\xd3\xf5\x00Y\xc7d\x82\xa4\x12\x16\xf3i=R\x1dS=j_N\xe9\xea\xb44`{pC\xacG\xcb\x9a',
                'transaction_root': b'tx_list tx_list tx_list tx_list ',
                'coinbase': b'~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdf',
                'state_root': b'post_stapost_stapost_stapost_sta',
                'receipt_root': b'receipt receipt receipt receipt ',
                'number': 2,
            },  # noqa: E501
        ),
    ),
)
def test_from_bytes_valid_bytes_length(header_bytes, expected_header_dict):
    actual_collation_header = CollationHeader.from_bytes(header_bytes)
    expected_collation_header = CollationHeader(**expected_header_dict)
    assert actual_collation_header == expected_collation_header


@pytest.mark.parametrize(
    'header_bytes',
    (
        b'',
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x06\xd0x\t\x1a\xc1\xff!l\x19@\xd0T\x0fX\xd3!Ny\x89\xc3\x1dg\xa36\x11\xd5\x00j\x92\xb5\xd5\xeb\xd3\xf5\x00Y\xc7d\x82\xa4\x12\x16\xf3i=R\x1dS=j_N\xe9\xea\xb44`{pC\xacG\xcb\x9atx_list tx_list tx_list tx_list \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdfpost_stapost_stapost_stapost_stareceipt receipt receipt receipt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x02',  # noqa: E501
        b'\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x05\xbd&\xfb\x06L\x1c\x85\xc9\x14\xad%\xfb\xbc\xfc\xef\xc5\x8bW\xe7\xaaJ\x91N\x9cj\xd0\x19n\xd7\xe1u\xc6\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00tx_list tx_list tx_list tx_list \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00~_ER\t\x1ai\x12]]\xfc\xb7\xb8\xc2e\x90)9[\xdfpost_stapost_stapost_stapost_stareceipt receipt receipt receipt \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x01',  # noqa: E501
    ),
    ids=('zero_length', 'one_byte_missing', 'one_item_missing'),
)
def test_from_bytes_invalid_bytes_length(header_bytes):
    with pytest.raises(ValidationError):
        CollationHeader.from_bytes(header_bytes)
