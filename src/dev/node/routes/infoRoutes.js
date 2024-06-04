const express = require('express');
const router = express.Router();
const infoController = require('../controllers/infoController');

router.get('/api/info', infoController.getInfo);
router.get('/', infoController.renderIndex);

module.exports = router;