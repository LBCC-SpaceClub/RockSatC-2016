#include "mcp3008Spi.h"
#include <time.h>
#include <chrono>

using namespace std::chrono;

void readGamma(int *retArr, int i, const int end_i, mcp3008Spi *adc){
	// Reads several channels from an ADC, saves them into an array
	unsigned char temp[3];
	// Send a start byte (1), second byte (channel), third byte (don't care)
	for(; i<end_i; i++){
		cout << i;
		temp[0] = 1;
		temp[1] = 0b10000000 | (i << 4);
		int t1 = temp[1];
		temp[2] = 0;
		// spiWriteRead() changes the value of temp
	        adc->spiWriteRead(temp, sizeof(temp) );
		// Update the array based on the new readings
	        retArr[i] = ((temp[1] << 8) & 0b1100000000) | (temp[2] & 0xff);
		//printf("i=%d, t1=%d, t[1]=%d, t[2]=%d, v=%d\n",i,t1,temp[1],temp[2],retArr[i]);
	}
}
 
int main(void)
{
	cout << "Running some tests.." << endl;
	// Each ADC can read up to 8 detectors
	mcp3008Spi adc_0("/dev/spidev0.0", SPI_MODE_0, 1000000, 8);
	mcp3008Spi adc_1("/dev/spidev0.1", SPI_MODE_0, 1000000, 8);
	const int numChan_0 = 6; // Share the 12 detectors between both ADC's
	const int numChan_1 = 6;
	int data[12];
	const unsigned int sampleSize = 1;

	for(unsigned int i=0; i<sampleSize; i++){
		readGamma(data, 0, numChan_0, &adc_0);
		readGamma(data, numChan_0, numChan_0+numChan_1, &adc_1);
		printf("Sample %d:", i);
		for(int j=0; j<numChan_0+numChan_1; j++){
			cout << "  " << data[j];
		}
		cout << ".\n";
	}
	return 0;
}
