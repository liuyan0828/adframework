Directory Structure Overview

libs (Libraries)
  CompareXml: Compares differences between two XML files
  Config: Basic configuration file
  GetAdData: Retrieves ad request response data
  GetAdConf: Fetches Mango configuration based on ad group ID
  CheckResult: Validates test results

utils (Utility Modules)
  LogHandler: Encapsulated logging module
  ReadYaml: Reads YAML files
  MakeDir: Creates directories
  readExpectedResult: Reads expected result files
  RequestsHandler: Encapsulated HTTP request module (requests)
  UrlHandler: URL processing module
  Xxtea: Encryption and decryption method

Script (Test Scripts)
  Stores test case YAML files along with corresponding baseline JSON/XML files.

TestCase (Test Cases)
  Stores test cases with the following naming conventions:

Test modules: Start with test_
Test classes: Start with Test
Test methods: Start with test_
For example, the test_open test case only requires modifying the YAML file path to execute.
Report (Test Reports)
Stores test execution reports.

Standalone Scripts
  SendAlert.py: Sends alert notifications when Jenkins test execution fails
  main.py: Main execution file. Run main.py to execute all test cases. To run a specific test case, specify the module or method to execute.
