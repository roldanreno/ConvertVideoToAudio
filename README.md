# ConvertVideoToAudio
AWS Lambda to extract mp3 from video using AWS Elemental MediaConvert.

This lambda requires 4 Env Variables:

DESTINATION: Amazon S3 path destionation of the mp3 file".
QUEUE: Previously created AWS Elemental MediaConvert Queue.
REGION: AWS prefered region.
ROLE: AWS Elemental MediaConvert Service Role
