#include <iostream>
#include <cstring>
#include <iomanip>
#include <cstdlib>
#include <string>
#include <cctype> // NO other #include are allowed!
using namespace std; // NO other using are allowed!
    // global
    string s = "ACBACBAB";

    string pattern_match(string& sline) {
        if (sline.length() == 0)
            return "";

        string spass;
        string sret;
        if (sline.length()>3) {
            if (sline.substr(0, 4) == "ACBA") {
                spass = sline.substr(4);
                sret = pattern_match(spass);
                if (sret == "mapping not possible") {
                    if (sline.substr(0, 3) == "BAB") {
                        spass = sline.substr(3);
                        sret = pattern_match(spass);
                        if (sret == "mapping not possible") {
                            if (sline.length()>1) {
                                if (sline.substr(0, 2) == "AC") {
                                    spass = sline.substr(2);
                                    sret = pattern_match(spass);
                                    if (sret == "mapping not possible") {
                                        return "mapping not possible";
                                    }
                                    else {
                                        return 'Z' + sret;
                                    }
                                }
                            }
                        } else {
                            return "Y" + sret;
                        }

                    }
                }
                else {
                    return "X" + sret;
                }
            }
        }
        if (sline.length()>2) {
            if (sline.substr(0, 3) == "BAB") {
                spass = sline.substr(3);
                sret = pattern_match(spass);
                if (sret == "mapping not possible") {
                    if (sline.length()>1) {
                        if (sline.substr(0, 2) == "AC") {
                            spass = sline.substr(2);
                            sret = pattern_match(spass);
                            if (sret == "mapping not possible") {
                                return "mapping not possible";
                            }
                            else {
                                return 'Z' + sret;
                            }
                        }
                    }
                } else {
                    return "Y" + sret;
                }

            }
        }
        if (sline.length()>1) {
            if (sline.substr(0, 2) == "AC") {
                spass = sline.substr(2);
                sret = pattern_match(spass);
                if (sret == "mapping not possible") {
                    return "mapping not possible";
                }
                else {
                    return 'Z' + sret;
                }
            }
        }
        return "mapping not possible";
    }

int main()
{
    s = pattern_match(s);
    cout << s; // Display the output string (after translation).

    return 0;
}


