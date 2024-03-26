
// 创建WebSocket连接  
const socket = new WebSocket('ws://192.168.0.111:8765');

// 处理连接打开事件  
socket.onopen = function (event) {
    console.log('Connected to WebSocket server');
};

// 处理接收到的消息事件  
socket.onmessage = function (event) {
    const messageList = document.getElementById('messages');
    const messageElement = document.createElement('li');
    messageElement.textContent = event.data;
    messageList.appendChild(messageElement);
};

let isMoving = false;
let acceleration = 0;
// 最大速度
const MAX_SPEED = 100;
// 加速速率
const RATE = 5;

// 处理连接关闭事件  
socket.onclose = function (event) {
    console.log('Disconnected from WebSocket server');
};

// 处理错误事件  
socket.onerror = function (event) {
    console.error('WebSocket error observed:', event);
};

function sendJsonMessage() {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            name: 'John Doe',
            age: 30,
            message: 'Hello from client!'
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.');
    }
}



function cameraRotate(direction) {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            topic: 'camera',
            direction,
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.');
    }

}

function sendForwardMsg(speed) {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            topic: 'wheel',
            direction: 'front',
            speed,
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.');
    }

}

function sendBackMsg(speed) {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            topic: 'wheel',
            direction: 'back',
            speed,
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.');
    }

}

function sendStopMsg() {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            topic: 'wheel',
            direction: 'stop',
            speed: 0,
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.');
    }
}

var accelerationInterval;
var decelerateInterval;
const frontButton = document.getElementById('front');
const  backButton = document.getElementById('back');

frontButton.addEventListener('mousedown', () => {
    isMoving = true;
    acceleration = 10;
    accelerationInterval = window.setInterval(() => {
        if (acceleration < MAX_SPEED) {
            acceleration += RATE;
        }
        sendForwardMsg(acceleration);

    }, 200)

    const decelerateAndStop = () => {
        if (accelerationInterval) {
            window.clearInterval(accelerationInterval);
        }
        decelerateInterval = window.setInterval(() => {
            if (acceleration > 0 && acceleration) {
                acceleration -= RATE;

                sendForwardMsg(acceleration)
            } else {
                if (decelerateInterval) {
                    window.clearInterval(decelerateInterval)
                }
                isMoving = false;
                sendStopMsg();

            }
        }, 200)
    }
    frontButton.addEventListener('mouseup', decelerateAndStop, { once: true });


})

backButton.addEventListener('mousedown', () => {
    isMoving = true;
    acceleration = 10;
    accelerationInterval = window.setInterval(() => {
        if (acceleration < MAX_SPEED) {
            acceleration += RATE;
        }
        sendBackMsg(acceleration);

    }, 200)

    const decelerateAndStop = () => {
        if (accelerationInterval) {
            window.clearInterval(accelerationInterval);
        }
        decelerateInterval = window.setInterval(() => {
            if (acceleration > 0 && acceleration) {
                acceleration -= RATE;

                sendBackMsg(acceleration)
            } else {
                if (decelerateInterval) {
                    window.clearInterval(decelerateInterval)
                }
                isMoving = false;
                sendStopMsg();

            }
        }, 200)
    }
    backButton.addEventListener('mouseup', decelerateAndStop, { once: true });


})

function stop() {
    isMoving = false;
    acceleration = 0;
    console.log(' -- stop');
    if (accelerationInterval) {
        window.clearInterval(accelerationInterval);
    }

    if (decelerateInterval) {
        window.clearInterval(decelerateInterval)
    }
    sendStopMsg();

}