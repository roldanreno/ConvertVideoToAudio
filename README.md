# ConvertVideoToAudio
An Amazon S3 trigger that retrieves metadata for the video object that has been updated then extract audio in mp3 using AWS Elemental MediaConvert.

This lambda requires 4 Env Variables:

## DESTINATION: Amazon S3 path destionation of the mp3 file".
## QUEUE: Previously created AWS Elemental MediaConvert Queue.
## REGION: AWS prefered region.
## ROLE: AWS Elemental MediaConvert Service Role
