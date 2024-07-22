# Speech Processing System

This project is a distributed speech processing system that consists of two main services: a Transcription Service and a Natural Language Understanding (NLU) Service. The system uses gRPC for inter-service communication and is containerized using Docker.

## System Architecture

The system consists of two microservices:
1. Transcription Service: Converts audio input to text.
2. NLU Service: Analyzes the transcribed text for sentiment and intent.

Both services communicate via gRPC and use SSL/TLS for secure communication.

## Prerequisites

- Docker
- Docker Compose
- Python 3.12
- OpenSSL (for generating SSL certificates)

## Setup

1. Clone the repository:
   ```
   git clone https://github.com/yourusername/speech-processing-system.git
   cd speech-processing-system
   ```

2. Generate SSL certificates:
   ```bash
   mkdir ssl
   cd ssl
   
   # Generate CA
   openssl genrsa -out ca.key 4096
   openssl req -new -x509 -key ca.key -sha256 -subj "/C=TR/ST=Istanbul/O=MyOrg, Inc." -days 365 -out ca.cert

   # Generate server certificate
   openssl genrsa -out server.key 4096
   openssl req -new -key server.key -out server.csr -config ssl.conf
   openssl x509 -req -in server.csr -CA ca.cert -CAkey ca.key -CAcreateserial -out server.cert -days 365 -sha256 -extfile ssl.conf -extensions req_ext

   # Generate client certificate (if needed)
   openssl genrsa -out client.key 4096
   openssl req -new -key client.key -out client.csr -config ssl.conf
   openssl x509 -req -in client.csr -CA ca.cert -CAkey ca.key -CAcreateserial -out client.cert -days 365 -sha256 -extfile ssl.conf -extensions req_ext
   ```

   Note: Make sure to create an `ssl.conf` file with appropriate configurations before running these commands.
3. Place models in service folders (`nlu/model` and `transcription/model`)
4. Build and run the services:
   ```bash
   docker-compose up --build
   ```

## Usage

The system exposes two gRPC services:

1. Transcription Service on port 50051
2. NLU Service on port 50052

To use the system, you need to implement a gRPC client that sends audio data to the Transcription Service and receives the analyzed results from the NLU Service.

Example client usage (pseudo-code):

```python
# Connect to Transcription Service
transcription_stub = create_secure_channel('localhost:50051')

# Send audio data
transcription_stream = transcription_stub.StreamTranscription(audio_data)

# Connect to NLU Service
nlu_stub = create_secure_channel('localhost:50052')

# Send transcript for analysis
nlu_results = nlu_stub.AnalyzeText(transcription_stream)

for result in nlu_results:
  print(f"Sequence: {result.sequence_number}, "
        f"Sentiment: {result.sentiment}, "
        f"Intention: {result.intention}")
```

## Development

### Project Structure

```
speech-processing-system/
├── docker-compose.yml
├── transcription/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── model
│   └── src/
│       └── server.py
├── nlu/
│   ├── Dockerfile
│   ├── requirements.txt
│   ├── model
│   └── src/
│       └── server.py
└── ssl/
    ├── ca.cert
    ├── server.key
    └── server.cert
```

### Adding New Features

1. To add features to a service, modify the corresponding `server.py` file.
2. Update the `requirements.txt` file if you add new dependencies.
3. If you change the gRPC service definition, update the `.proto` files and regenerate the gRPC code.

## Troubleshooting

- If you encounter SSL-related issues, ensure that the certificates are correctly generated and placed in the `ssl/` directory.
- For gRPC communication issues, check if the services are running and listening on the correct ports.
