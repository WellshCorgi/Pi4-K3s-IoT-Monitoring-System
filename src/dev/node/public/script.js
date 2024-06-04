function formatBytes(bytes) {
    const units = ['B', 'KB', 'MB', 'GB', 'TB'];
    if (bytes === 0) return '0 B';
    const i = Math.floor(Math.log(bytes) / Math.log(1024));
    return parseFloat((bytes / Math.pow(1024, i)).toFixed(2)) + ' ' + units[i];
}

async function fetchData() {
    try {
        const response = await fetch('/api/info');
        const data = await response.json();

        const cpuUsage = data.cpu_percent || 'N/A';
        const ramTotal = data.ram_total || 'N/A';
        const ramUsed = data.ram_used || 'N/A';
        const ramFree = data.ram_free || 'N/A';

        let ramUsedPercentage = 'N/A';
        if (ramTotal !== 'N/A' && ramUsed !== 'N/A') {
            ramUsedPercentage = ((ramUsed / ramTotal) * 100).toFixed(2) + '%';
        }

        // RAM 값을 사람이 읽을 수 있는 형식으로 변환
        const ramTotalFormatted = ramTotal !== 'N/A' ? formatBytes(ramTotal) : 'N/A';
        const ramUsedFormatted = ramUsed !== 'N/A' ? formatBytes(ramUsed) : 'N/A';
        const ramFreeFormatted = ramFree !== 'N/A' ? formatBytes(ramFree) : 'N/A';

        document.getElementById('cpu-info').innerText = `CPU 정보: 현재 사용률 - ${cpuUsage}%`;
        document.getElementById('ram-info').innerText = `RAM 정보: 총 용량 - ${ramTotalFormatted}, 사용 중 - ${ramUsedFormatted} (${ramUsedPercentage}), 사용 가능 - ${ramFreeFormatted}`;
    } catch (error) {
        console.error('데이터 가져오기 오류', error);
    }
}

// 0.5초마다 fetchData 함수를 호출하여 실시간으로 데이터 갱신
setInterval(fetchData, 500);

// 페이지가 로드될 때 초기 데이터 가져오기
fetchData();
