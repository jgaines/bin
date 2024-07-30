#!/bin/env sh

# Simple script to test .dockerignore file.
# Run in the build context (where the .dockerignore file is), it'll create a temp
# image then dump out everything that ended up in it.  It'll leave you sitting at
# an sh prompt inside the container so you can poke around if you want.
# Once you exit the container, it removes the image.

# source: https://stackoverflow.com/questions/38946683/how-to-test-dockerignore-file
# Here's a sample build command you can use to create an image with the current folder's build context:

docker image build --no-cache -t build-context -f - . <<EOF
FROM busybox
WORKDIR /build-context
COPY . .
CMD find .
EOF

# Once created, run the container and inspect the contents of the /build-context directory which includes everything not excluded by the .dockerignore file:

#run the default find command
docker container run --rm build-context
#or inspect it from a shell using
docker container run --rm -it build-context /bin/sh

# You can then cleanup with:

docker image rm build-context

