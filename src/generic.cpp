
#ifndef __lazo_generic__
#define __lazo_generic__

#include <bits/stdc++.h>
#include "json/single_include/nlohmann/json.hpp"

#define FOR(i,a,b) for (int i = (int)(a); i < (int)(b); ++i)
#define REP(i,n) FOR(i,0,n)
#define x first
#define y second

using namespace std;
using json = nlohmann::json;

const string samples_group = "../../samples_by_packer_group.txt";
const string samples = "../../samples";
const string reports = "../../reports";

vector<string> hashes;
unordered_map<string, int> labels;
vector<string> groups[5];

const double eps = 1e-6;

string getSample(string hash){
  string location = samples + "/" + hash.substr(hash.size()-2) + "/" + hash;
  ifstream in(location);
  stringstream sin;
  sin << in.rdbuf();
  return sin.str();
}

json getReport(string hash){
  string location = reports + "/" + hash.substr(hash.size()-2) + "/" + hash + ".json";
  ifstream in(location);
  json output;
  in >> output;
  return output;
}

void loadData(){
  ifstream in(samples_group);
  string tmp;
  while (in >> tmp){
    string hash = tmp;
    hash.pop_back();
    hash.pop_back();
    int label = tmp.back() - '0';
    hashes.push_back(hash);
    labels[hash] = label;
    groups[label].push_back(hash);
  }
}

int randInt(int lo, int hi){
  return rand() % (hi - lo + 1) + lo;
}

string getRandomHash(int src = -1){
  if (src == -1) return hashes[randInt(0, (int)hashes.size()-1)];
  else return groups[src][randInt(0, (int)groups[src].size()-1)];
}

double entropy(const vector<double> &freq){
  double sum = 0;
  for (auto t : freq) sum += t;
  double output = 0;
  for (auto t : freq){
    t /= sum;
    if (t > eps) output -= t * log(t);
  } return output;
}

double quantile(vector<double> v, double q){
  sort(v.begin(), v.end());
  q = q * ((int)v.size()-1);
  int id = (int)q;
  double del = q-id;
  return v[id] * (1-del) + v[id+1] * del;
}

double median(const vector<double> &v){
  return quantile(v, 0.5);
}

double IRQ(const vector<double> &v){
  return quantile(v, 0.75) - quantile(v, 0.25);
}

double expected(const vector<double> &v){
  double output = 0;
  for (auto t : v) output += t;
  return output / (double)v.size();
}

double pot(double x, int y){
  double r = 1;
  while (y){
    if (y&1) r *= x;
    x *= x, y >>= 1;
  } return r;
}

double centralMoment(const vector<double> &v, int t){
  double e = expected(v);
  double output = 0;
  for (auto f : v)
    output += pot(f-e, t);
  return output / (double)v.size();
}

double covariance(const vector<double> &a, const vector<double> &b){
  double ae = expected(a);
  double be = expected(b);
  double output = 0;
  REP(i,a.size()) output += (a[i] - ae) * (b[i] - be);
  return output / ((int)a.size()-1);
}

double stdDev(const vector<double> &v){
  return sqrt(covariance(v, v));
}

double correlation(const vector<double> &a, const vector<double> &b){
  return covariance(a, b) / stdDev(a) / stdDev(b);
}

double skewness(const vector<double> &v){
  if (stdDev(v) == 0) return 0;
  return centralMoment(v, 3) / pot(stdDev(v), 3);
}

#endif
