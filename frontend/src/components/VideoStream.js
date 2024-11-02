import React, { useEffect, useRef } from 'react';

const VideoStream = () => {
  const videoRef = useRef(null);

  useEffect(() => {
    const host = process.env.REACT_APP_WS_HOST || 'localhost';
    const port = process.env.REACT_APP_WS_PORT || 8888;
    
    const ws = new WebSocket(`ws://${host}:${port}/ws`);

    ws.onmessage = (event) => {
      const blob = new Blob([event.data], { type: 'image/jpeg' });
      const url = URL.createObjectURL(blob);
      if (videoRef.current) {
        videoRef.current.src = url;
      }
    };

    return () => {
      ws.close();
    };
  }, []);

  return (
    <div>
      <h1>Video Stream</h1>
      <img ref={videoRef} alt="Video Stream" />
    </div>
  );
};

export default VideoStream;