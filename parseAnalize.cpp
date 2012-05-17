#include <iostream>
#include <fstream>
#include <string>
using namespace std;

int main(){
  ifstream inputFile;
  ofstream outputFile;
  inputFile.open("inputFile.txt",ios::in);
  outputFile.open("outputFile.txt",ios::out);
  string line;
  if(inputFile.is_open() && outputFile.is_open()){
    
    while(inputFile.good()){
        getline(inputFile,line);
        outputFile << line;
      }
    
    inputFile.close();
    outputFile.close();
  }
  return 0;
}
