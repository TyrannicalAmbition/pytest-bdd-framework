import pytest
from pytest_bdd import scenario


@pytest.mark.ui
@scenario("features/login_form.feature", "Login form elements are visible")
def test_login_form_visibility():
    pass


@pytest.mark.ui
@scenario("features/login_form.feature", "Successful login with valid credentials")
def test_successful_login():
    pass


@pytest.mark.ui
@scenario("features/login_form.feature", "Fill login form fields")
def test_fill_login_form_fields():
    pass


@pytest.mark.ui
@scenario("features/login_form.feature", "Login with invalid email format")
def test_login_with_invalid_email():
    pass


@pytest.mark.ui
@scenario("features/login_form.feature", "Login with invalid credentials")
def test_login_with_invalid_credentials():
    pass
