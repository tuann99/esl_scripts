const express = require('express');
const { createProxyMiddleware } = require('http-proxy-middleware');

const app = express();

app.use('/', createProxyMiddleware({ 
    target: 'https://geocoding.geo.census.gov', 
    changeOrigin: true,
    pathRewrite: (path, req) => {
        return '/geocoder/locations/onelineaddress' + path;
    },
    onProxyReq: (proxyReq, req, res) => {
        const rewrittenPath = '/geocoder/locations/onelineaddress' + req.url;
        console.log('Request URL:', proxyReq.getHeader('host') + rewrittenPath);
    },
}));

const port = 3000;
app.listen(port, () => console.log(`Proxy server running on port ${port}`));