#include "mcp3008Spi.h"
#include <iostream>
#include <fstream>
//#include <time.h>
#include <chrono>

using namespace std;
using hr_clock = std::chrono::high_resolution_clock;
using micros = std::chrono::milliseconds;

int main(void)
{
	// Create a filename from the date and time
	time_t t = time(0);
	struct tm * now = localtime ( &t );
	char filename [80];
	strftime (filename, 80, "dlog_%F_%R.txt", now);

	ofstream log(filename);
	if(log.is_open()){
		cout << "Log file successfully opened." << endl;
	} else {
		cout << "Emergency: log file cannot be opened." << endl;
	}

	// Each ADC can read up to 8 detectors
        mcp3008Spi adc_0("/dev/spidev0.0", SPI_MODE_0, 1000000, 8);
        mcp3008Spi adc_1("/dev/spidev0.1", SPI_MODE_0, 1000000, 8);
        const int numChan_0 = 6; // Share the 12 detectors between both ADC's
        const int numChan_1 = 6;
	const unsigned long run_time = 1000; // how long the program runs, in milliseconds
        unsigned char data[3];	// a buffer to store SPI data in
        int val;		// a buffer to store a single SPI result
        string line;		// a buffer to store the combined SPI results

	// Timestamp stuff
        hr_clock::time_point start_time = hr_clock::now();
        unsigned long cur_time = std::chrono::duration_cast<micros>(hr_clock::now() - start_time).count();

	// Write a header to the log file.  This should be improved to a datetime stamp.
        log << "Log begins at "+to_string(cur_time)+" microseconds.\n";

	while(cur_time < run_time){
		// Refresh the current timestamp
		cur_time = std::chrono::duration_cast<micros>(hr_clock::now() - start_time).count();
		log << to_string(cur_time)+',';
        	for(int i=0; i<12; i++){
        		data[0] = 1;
        		data[1] = 0b10000000 | (i << 4);
        		data[2] = 0;

			if(i<6){
	        		adc_0.spiWriteRead(data, sizeof(data) ); // detectors 0-5
			}else{
				adc_1.spiWriteRead(data, sizeof(data) ); // detectors 6-11
			}

        		val = ((data[1] << 8) & 0b1100000000) | (data[2] & 0xff);
        		line.append(to_string(val)+',');
        	}
		// Visible output here is only for debugging
		//cout << "Sample " << s << " = " << line << endl;
		log << line + '\n';
		line = "";
        }
        return 0;
}
