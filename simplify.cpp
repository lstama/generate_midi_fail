#include <bits/stdc++.h>
#define vs vector<string>
#define iv pair<int,vs >
using namespace std;
vector<iv> notes;
int channelCount[129];
long long channelTotal[129];

int main(){
    ios::sync_with_stdio(0);
    string now,before;
    bool first = 1;
    int tempo;
    while (cin >> now){
        string temp = now;
        transform(temp.begin(), temp.end(), temp.begin(), ::tolower);
        if (temp == "tempo" && first == 1){
            first = 0;
            cin >> tempo;
        }
        if (temp == "note_on_c"){
            int time;
            vector<string> vtmp;
            vtmp.clear();
            istringstream ( before ) >> time;
            vtmp.push_back(temp);
            cin >> temp;
            vtmp.push_back(temp);
            cin >> temp;
            vtmp.push_back(temp);
            cin >> temp;
            vtmp.push_back(temp);
            notes.push_back(iv(time,vtmp ) );
        } else
        if (temp == "note_off_c"){
            int time;
            vector<string> vtmp;
            vtmp.clear();
            istringstream ( before ) >> time;
            vtmp.push_back("note_on_c");
            cin >> temp;
            vtmp.push_back(temp);
            cin >> temp;
            vtmp.push_back(temp);
            cin >> temp;
            vtmp.push_back("0");
            notes.push_back(iv(time,vtmp ) );
        }
        before = now;
    }
    //sort(notes.begin(),notes.end());
    vector <int> deletedChannel; deletedChannel.push_back(9);deletedChannel.push_back(10);

    int si = notes.size();
    for (int i = 0; i < si; i++){
        if (notes[i].second[0] == "note_on_c" || notes[i].second[0] == "note_off_c"){
            int ch,no;
            istringstream ( notes[i].second[1] ) >> ch;
            istringstream ( notes[i].second[2] ) >> no;
            if (ch == 9) continue;
            channelCount[ch-1] = channelCount[ch-1] + 1;
            channelTotal[ch-1] = channelTotal[ch-1] + no;
        }
    }

    vector<pair <double,int> > channelSorted;
    for (int i = 0; i < 128; i++){
        if (channelCount[i] > 0){
            pair <double,int> pr = pair <double,int>((double)channelTotal[i]/(double)channelCount[i],i);
            channelSorted.push_back(pr);
        }
    }

    int ukuran = channelSorted.size();
    int deleted = round((double)ukuran*(double)0.3);
    sort(channelSorted.begin(),channelSorted.end());
    if (ukuran > 4){
        for (int i = 0; i < deleted; i++){
            deletedChannel.push_back(channelSorted[i].second + 1);
        }
    }


    vector<bool> flag; flag.assign(si+1,1);

    for (int i = 0; i < notes.size(); i++){
        bool pass = 1;
        int ch;
        istringstream ( notes[i].second[1] ) >> ch;
        for (int j = 0; j < deletedChannel.size(); j++){
            if (ch == deletedChannel[j] ) pass = 0;
        }
        if (!pass) flag[i]=0;
    }
    cout << "time,channel,note,velocity\n";
    for (int i = 0; i < notes.size(); i++){
        if (!flag[i]) continue;
        //cout << "1, ";
        cout << notes[i].first;
        for (int j = 1; j < notes[i].second.size(); j++){
            //if (j == 1){
            //  cout << ", " << 1;
              //continue;
            //}
            cout << ", " << notes[i].second[j];
        }
        cout << endl;
    }
    return 0;
}
