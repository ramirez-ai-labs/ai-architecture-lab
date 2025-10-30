from unittest.mock import patch
import pytest

from app.service import AccountService, InsufficientFunds


def test_create_account_calls_repo_and_publishes_event():
    svc = AccountService()
    with patch('app.repository.create_account', return_value=123) as mock_create, \
         patch('app.repository.upsert_account_balance') as mock_upsert, \
         patch('app.events.publish') as mock_publish:
        aid = svc.create_account("Alice", 50.0)
        assert aid == 123
        mock_create.assert_called_once_with("Alice", 50.0)
        assert mock_publish.called
        mock_upsert.assert_called_once_with(123, 50.0)


def test_withdraw_insufficient_funds_raises():
    svc = AccountService()

    class FakeCursor:
        def execute(self, *args, **kwargs):
            return None

        def fetchone(self):
            return (5.0,)

    class FakeConn:
        def cursor(self):
            return FakeCursor()

        def commit(self):
            pass

        def close(self):
            pass

    with patch('app.repository.get_db_conn', return_value=FakeConn()):
        with pytest.raises(InsufficientFunds):
            svc.withdraw(1, 10.0)
