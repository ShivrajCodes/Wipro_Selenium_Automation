Feature: User Management API
  As an API consumer
  I want to create, read, update and delete users
  So that I can verify the User Management API behaves correctly

  Background:
    Given the API base URL is set

  @smoke @get
  Scenario: Get all users returns a valid list
    When I send a GET request to fetch all users
    Then the response status code should be 200
    And the response should match the "user_list_schema.json" schema
    And the response time should be under 2000 ms

  @get
  Scenario: Get a single existing user by ID
    When I send a GET request to fetch user with id 1
    Then the response status code should be 200
    And the response should match the "user_schema.json" schema
    And the response field "id" should equal 1

  @get @negative
  Scenario: Get a non-existent user returns 404
    When I send a GET request to fetch user with id 99999
    Then the response status code should be 404

  @post @create
  Scenario: Create a new user with valid data
    When I send a POST request to create a user with valid data
    Then the response status code should be 201
    And the response should match the "created_user_schema.json" schema
    And the response field "name" should equal "Shivraj Sharma"

  @put @update
  Scenario: Update an existing user
    When I send a PUT request to update user with id 1 with valid data
    Then the response status code should be 200
    And the response field "name" should equal "Shivraj S. Updated"

  @delete
  Scenario: Delete an existing user
    When I send a DELETE request to remove user with id 1
    Then the response status code should be 200
