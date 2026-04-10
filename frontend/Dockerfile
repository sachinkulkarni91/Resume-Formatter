FROM node:18-alpine

WORKDIR /app

# Copy package files
COPY frontend/package*.json ./

# Install dependencies
RUN npm install

# Copy source code
COPY frontend/ .

# Build application
RUN npm run build

# Expose port
EXPOSE 3000

# Use a lightweight server for production
RUN npm install -g serve

# Run production server
CMD ["serve", "-s", "dist", "-l", "3000"]
