FROM    virtual-library-builder

ADD     .   ./app
WORKDIR /app

ENV     LISTEN_ADDR="0.0.0.0" \
        LISTEN_PORT=7777

# Make port 7777 available to the world outside this container
EXPOSE   7777

RUN      chmod 755 ./entrypoint.sh

# Run the virtual_library flask app when the container launches
CMD ["./entrypoint.sh"]
