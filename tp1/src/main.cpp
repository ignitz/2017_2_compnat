#include <iostream>
#include "csv/csv.hpp"
#include "ga/ga.hpp"

void test_csv(std::string dataset) {
  Csv csv (dataset);
  if (csv.open_file())
  {
    csv.read();
    csv.close();
  }
  else {
    std::cout << "Deu tudo errado" << std::endl;
  }
  
};

// int argc, char const *argv[]
int main()
{
  test_csv("datasets/keijzer-10-train.csv");

  // test_csv("datasets/keijzer-10-test.csv");
  // test_csv("datasets/house-train.csv");
  // test_csv("datasets/house-test.csv");
  // test_csv("datasets/keijzer-7-train.csv");
  // test_csv("datasets/keijzer-7-test.csv");
  return 0;
}