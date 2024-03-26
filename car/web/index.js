
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

function sendCarMoveMsg(direction, speed) {
    if (socket.readyState === WebSocket.OPEN) {
        // 创建一个JSON对象  
        var jsonData = {
            topic: 'wheel',
            direction,
            speed,
        };

        // 将JSON对象转换为字符串  
        var jsonString = JSON.stringify(jsonData);

        // 发送JSON字符串给服务器  
        socket.send(jsonString);
        console.log('JSON message sent to server:', jsonData);
    } else {
        console.log('WebSocket is not open. Unable to send message.', direction, speed);
    }
}


var accelerationInterval;
var decelerateInterval;
const frontButton = document.getElementById('front');
const backButton = document.getElementById('back');

var speed = 0;

// 加速
function accelerate(direction) {
    isMoving = true;
    if (decelerateInterval) {
        window.clearInterval(decelerateInterval);
    }
    accelerationInterval = window.setInterval(() => {
        if (speed < MAX_SPEED) {
            speed += RATE;
        }
        sendCarMoveMsg(direction, speed);
    }, 200)
}

// 减速
function slowDown(direction) {
    console.log('-- mouse up', direction);

    if (accelerationInterval) {
        window.clearInterval(accelerationInterval);
    }

    decelerateInterval = window.setInterval(() => {

        speed = speed - RATE;
        if (speed > 0) {
            sendCarMoveMsg(direction, speed)
        } else {
            if (decelerateInterval) {
                window.clearInterval(decelerateInterval)
            }
            isMoving = false;
            speed = 0;
            stop();

        }
    }, 200)

}






function stop() {
    isMoving = false;
    speed= 0;
    console.log(' -- stop');
    if (accelerationInterval) {
        window.clearInterval(accelerationInterval);
    }

    if (decelerateInterval) {
        window.clearInterval(decelerateInterval)
    }
    sendCarMoveMsg('stop', 0);

}
var leftEl = document.getElementById('left');
var rightEl = document.getElementById('right')

const mql = window.matchMedia("(max-width:600px)");
console.log('Max width 6000px: ', mql);
if (mql.matches) {
    // mweb



    frontButton.addEventListener('touchstart', (e) => {
        e.preventDefault(); // 阻止默认行为  

        console.log('touch start');
        accelerate('front');
        frontButton.addEventListener('touchend',
            (e) => {
                e.preventDefault();

                slowDown('front')
            },
            { once: true });
    })

    backButton.addEventListener('touchstart', (e) => {
        e.preventDefault();
        accelerate('back');
        backButton.addEventListener('touchend', (e) => {

            e.preventDefault();
            slowDown('back')
        }, { once: true });
    })

    leftEl.addEventListener('touchstart', (e) => {
        e.preventDefault();
        stop();

        const time = window.setInterval(() => {

            sendCarMoveMsg('left', 30)
        }, 200)

        leftEl.addEventListener('touchend', (e) => {
            e.preventDefault();
            clearInterval(time);
            stop();

        }, { once: true })

    })

    rightEl.addEventListener('touchstart', (e) => {
        e.preventDefault();
        stop();

        const time = window.setInterval(() => {

            sendCarMoveMsg('right', 30)
        }, 200)

        rightEl.addEventListener('touchend', (e) => {
            e.preventDefault();
            clearInterval(time);
            stop();

        }, { once: true })
    })

} else {
    frontButton.addEventListener('mousedown', () => {
        accelerate('front');
        frontButton.addEventListener('mouseup', () => slowDown('front'), { once: true });
    })

    backButton.addEventListener('mousedown', () => {
        accelerate('back');
        backButton.addEventListener('mouseup', () => slowDown('back'), { once: true });
    })

    leftEl.addEventListener('mousedown', () => {
        stop();

        const time = window.setInterval(() => {

            sendCarMoveMsg('left', 30)
        }, 200)

        leftEl.addEventListener('mouseup', () => {
            clearInterval(time);
            stop();

        }, { once: true })

    })

    rightEl.addEventListener('mousedown', () => {
        stop();

        const time = window.setInterval(() => {

            sendCarMoveMsg('right', 30)
        }, 200)

        rightEl.addEventListener('mouseup', () => {
            clearInterval(time);
            stop();

        }, { once: true })
    })
}
