const infoModel = require('../models/infoModel');

const getInfo = (req, res) => {
    const data = infoModel.getLatestInfo();
    if (data) {
        res.json(data);
    } else {
        res.status(404).json({ error: '데이터가 없습니다' });
    }
};

const renderIndex = (req, res) => {
    res.render('index');
};

module.exports = {
    getInfo,
    renderIndex
};
