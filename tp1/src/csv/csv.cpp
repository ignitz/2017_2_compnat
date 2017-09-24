#include "csv.hpp"

using namespace std;

Csv::Csv (string filename) {
  cout << "Constructor" <<
  "\tfilename: " << filename << endl;
	this->filename = filename;
};

Csv::~Csv () {
  this->clear();
  this->close();
};

bool Csv::open_file() {
  myfile.open (filename, fstream::in);
  if (myfile.is_open())
  {
    return true;
  }

  cerr << "Error on opening file "
    << filename;
  return false;
}

void Csv::read() {
  string line;
  double aux;

  if (!data.empty()) {
    cerr << "data is not empty, clean data first" << endl;
    return;
  }

  if (myfile.is_open())
  {
    while ( !myfile.eof() ) {
      getline(myfile, line);
      vector<string> str_splited;
      vector<double> values;
      boost::split( str_splited, line, boost::is_any_of(",") );
      for ( auto value : str_splited ) {
        aux = atof(value.c_str());
        values.push_back(aux);
      }
      data.push_back(values);
    }
  }
};

void Csv::close() {
  myfile.close();
};

std::vector<std::vector<double>> Csv::get_data() {
  return data;
};

void Csv::clear() {
  data.clear();
};