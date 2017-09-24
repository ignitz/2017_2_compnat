#include <iostream>
#include <string>
#include <fstream>
#include <vector>

#include <boost/algorithm/string.hpp>

// #include <bits/stdc++>

class Csv
{
private:
  std::string filename;
  std::fstream myfile;
  std::vector<std::vector<double>> data;

public:
  Csv(std::string filename);
  virtual ~Csv();

  bool open_file ();
  void read ();
  void close ();
  void clear();

  std::vector<std::vector<double>> get_data();
};