const fs = require('fs');
const path = require('path');

// 读取swagger.json文件
const swaggerPath = path.join(__dirname, 'swagger.json');
const swagger = JSON.parse(fs.readFileSync(swaggerPath, 'utf8'));

// 消息回调相关的路径
const callbackPaths = [
  '/message/SetCallback',
  '/message/GetCallback',
  '/message/DeleteCallback'
];

// 修改paths顺序
const originalPaths = swagger.paths;
const newPaths = {};

// 1. 首先添加消息回调路径
callbackPaths.forEach(callbackPath => {
  const fullPath = callbackPath;
  if (originalPaths[fullPath]) {
    newPaths[fullPath] = originalPaths[fullPath];
  }
});

// 2. 添加其他路径
Object.keys(originalPaths).forEach(path => {
  if (!callbackPaths.includes(path)) {
    newPaths[path] = originalPaths[path];
  }
});

// 更新paths
swagger.paths = newPaths;

// 保存修改后的文件
fs.writeFileSync(swaggerPath, JSON.stringify(swagger));
console.log('Swagger JSON updated successfully!'); 