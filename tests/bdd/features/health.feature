Feature: Health check
  As a system administrator
  I want to verify the backend availability
  So that I can ensure the service is ready for students

  Scenario: Service returns ok
    Given the backend is running
    When I request the health endpoint
    Then I receive an ok status
