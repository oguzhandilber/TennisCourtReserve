# Use an official Nginx runtime as a parent image
FROM nginx:alpine

# Remove the default Nginx configuration file
RUN rm /etc/nginx/conf.d/default.conf

# Copy a custom Nginx configuration file (we will create this next)
COPY ./nginx.conf /etc/nginx/conf.d/default.conf

# Copy the static frontend files into the Nginx html directory
COPY . /usr/share/nginx/html

# Expose port 80 for the frontend
EXPOSE 80

# Start Nginx when the container launches
CMD ["nginx", "-g", "daemon off;"]

