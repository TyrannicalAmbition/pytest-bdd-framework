Feature: Login Form
  As a user
  I want to be able to log in to the application
  So that I can access my account

  Background:
    Given I am on the login page

  Scenario: Successful login with valid credentials
    When I fill in the email field with "pahibi5251@nicext.com"
    And I fill in the password field with "64B724$Xc"
    And I click the login button
    Then I should be logged in successfully

  Scenario: Login form elements are visible
    Then the login form should be visible
    And the email field should be empty
    And the password field should be empty

  Scenario: Fill login form fields
    When I fill in the email field with "user@test.com"
    And I fill in the password field with "secret123"
    Then the email field should contain "user@test.com"
    And the password field should contain "secret123"

  Scenario: Login with invalid email format
    When I fill in the email field with "invalid-email"
    And I fill in the password field with "password123"
    And I click the login button
    Then I should see email validation error

  Scenario: Login with invalid credentials
    When I fill in the email field with "user@test.com"
    And I fill in the password field with "secret123"
    And I click the login button
    Then I should see validation error