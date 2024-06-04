const express = require('express');
const app = express();
const path = require('path');
const { Stream } = require('node-rtsp-stream')
const infoRoutes = require('./routes/infoRoutes');
const infoModel = require('./models/infoModel');
const port = 3300;

// 서버 실행 시, RabbitMQ 연결 
infoModel.connectRabbitMQ(() => {
    console.log('RabbitMQ 연결 성공');
});

app.set('view engine', 'ejs');
app.set('views', path.join(__dirname, 'views'));

// 정적 파일 서빙
app.use(express.static(path.join(__dirname, 'public')));

// 라우트 설정
app.use('/', infoRoutes);

app.listen(port, () => {
    console.log(`Server is running on http://localhost:${port}`);
});
