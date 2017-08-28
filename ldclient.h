/*
Transmits raw POV led data to a server
*/


#ifndef LDCLIENT_H
#define LDCLIENT_H

#ifdef __cplusplus
extern "C" {
#endif

// Returns 0 if successful
int LDconnect(const char * const pszServerURL);

// Returns 0 if successful
int LDTransmit(const char * const pData, int bytes);

// Returns 0 if ack was received from server before timeout
int LDWaitforAck();

void LDDisconnect();

#ifdef __cplusplus
}
#endif

#endif // LDCLIENT_H

