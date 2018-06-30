#include "generic.cpp"

json standardFeatures(const vector<double> &v){
  json output;
  output["expected"] = expected(v);
  output["median"] = median(v);
  output["IRQ"] = IRQ(v);
  output["stdDev"] = stdDev(v);
  output["ql"] = quantile(v, 0.25);
  output["qr"] = quantile(v, 0.75);
  output["skewness"] = skewness(v);
  return output;
}

vector<double> localEntropies(const string &exe, int sampleSize = 100, int bucket = 500){
  if (exe.empty()) return {0, 0, 0};
  bucket = min(bucket, (int)exe.size());
  vector<double> output;
  REP(blatruc, sampleSize){
    int start = randInt(0, (int)exe.size() - bucket);
    int cnt[256] = {};
    REP(i,bucket)
      ++cnt[(exe[start+i]+256)%256];
    vector<double> input;
    for (auto t : cnt)
      if (t) input.push_back(t);
    output.push_back(entropy(input));
  }
  return output;
}

double startEntropy(const string &exe, int bucket = 200){
  int cnt[256] = {};
  REP(i,min(bucket, (int)exe.size()))
    ++cnt[(exe[i]+256)%256];
  vector<double> input;
  for (auto t : cnt)
    if (t) input.push_back(t);
  return entropy(input);
}

vector<double> frequency(const string &exe){
  int cnt[256] = {};
  for (auto t : exe)
    ++cnt[(t+256)%256];
  vector<double> output;
  sort(cnt, cnt+256);
  REP(i,20)
    output.push_back(cnt[255-i] / (double)exe.size());
  return output;
}

int main(){
  srand(123456);

  string location;
  cin >> location;
  ifstream in(location);
  stringstream sin;
  sin << in.rdbuf();
  string exe = sin.str();
  
  json output;
  output["localEntropies"] = standardFeatures(localEntropies(exe));
  for (auto bucket : {50, 100, 150})
    output["startEntropy"][bucket] = startEntropy(exe, bucket);
  output["frequency"] = standardFeatures(frequency(exe));
  cout << output << endl;

  return 0;
}
