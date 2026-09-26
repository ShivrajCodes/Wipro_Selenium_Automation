Feature: Authentication
  As an API consumer
  I want to log in with valid and invalid credentials
  So that I can verify the API handles authentication correctly

  @auth @positive
  Scenario: Login with valid credentials succeeds
    Given the auth API base URL is set
    When I send a login request with valid credentials
    Then the auth response status code should be 200

  @auth @negative
  Scenario: Login with invalid credentials fails
    Given the auth API base URL is set
    When I send a login request with invalid credentials
    Then the auth response status code should be 200
    And the auth response message should indicate login failure
