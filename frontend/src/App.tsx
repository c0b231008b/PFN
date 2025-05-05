import React, { useState } from 'react';
import './App.css';

const MAX_LENGTH = 800;

function App() {
  const [inputText, setInputText] = useState('');
  const [originalText, setOriginalText] = useState('');
  const [correctedText, setCorrectedText] = useState('');
  const [isLoading, setIsLoading] = useState(false);
  const [toastMessage, setToastMessage] = useState('');
  const [errorMsg, setErrorMsg] = useState('');

  /* コピー関数（前回と同じ） */
  const copyToClipboard = async (text: string) => {
    try {
      await navigator.clipboard.writeText(text);
      setToastMessage('コピーしました！');
      setTimeout(() => setToastMessage(''), 2000);
    } catch {
      alert('コピーに失敗しました');
    }
  };

  /* 校閲実行 */
  const handleProofread = async () => {
    if (!inputText.trim()) return;

    setOriginalText(inputText);
    setInputText('');
    setCorrectedText('');
    setErrorMsg('');
    setIsLoading(true);

    try {
      const res = await fetch('http://localhost:8000/proofread', {
        method: 'POST',
        headers: { 'Content-Type': 'application/json' },
        body: JSON.stringify({ text: inputText }),
      });

      if (!res.ok) throw new Error(`status ${res.status}`);

      const data = await res.json();
      setCorrectedText(data.corrected_text);
    } catch (e) {
      console.error(e);
      setErrorMsg('サーバーとの通信に失敗しました。もう一度お試しください。');
    } finally {
      setIsLoading(false);
    }
  };

  /* 文字数の残量 */
  const remaining = MAX_LENGTH - inputText.length;
  const counterStyle = {
    color: remaining < 0 ? 'red' : remaining < 50 ? '#d97706' : '#555',
    fontSize: '14px',
    marginTop: '4px',
  } as const;

  return (
    <div style={{ maxWidth: 900, margin: '2rem auto', fontFamily: 'sans-serif' }}>
      <h2>文章校正ツール</h2>

      {/* 入力エリア */}
      <textarea
        placeholder={`文章を入力（最大${MAX_LENGTH}文字）`}
        maxLength={MAX_LENGTH}
        rows={10}
        style={{ width: '100%', fontSize: '16px', padding: '1rem' }}
        value={inputText}
        onChange={(e) => setInputText(e.target.value)}
      />
      {/* 文字数カウント */}
      <div style={counterStyle}>
        {inputText.length}/{MAX_LENGTH} 文字
      </div>

      {/* 校閲ボタン */}
      <button
        onClick={handleProofread}
        style={{ marginTop: '1rem', padding: '0.5rem 1rem', fontSize: '16px' }}
        disabled={isLoading}
      >
        校閲
      </button>

      {/* バックエンド処理中のメッセージ */}
      {isLoading && <p style={{ marginTop: '8px' }}>校閲中です…</p>}

      {/* エラーメッセージ */}
      {errorMsg && (
        <div
          style={{
            marginTop: '1rem',
            padding: '0.75rem 1rem',
            background: '#fee2e2',
            color: '#b91c1c',
            borderRadius: 6,
          }}
        >
          {errorMsg}
        </div>
      )}

      {/* 校正結果 */}
      {correctedText && (
        <div style={{ marginTop: '2rem' }}>
          <h3>校正結果</h3>
          <div style={{ display: 'flex', gap: '2rem' }}>
            {/* 校正前 */}
            <div style={{ flex: 1, position: 'relative' }}>
              <h4>校正前</h4>
              <button
                onClick={() => copyToClipboard(originalText)}
                style={{
                  position: 'absolute',
                  right: 0,
                  top: 0,
                  padding: '0.25rem 0.5rem',
                  fontSize: '12px',
                }}
              >
                コピー
              </button>
              <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '1rem' }}>
                {originalText}
              </div>
            </div>

            {/* 校正後 */}
            <div style={{ flex: 1, position: 'relative' }}>
              <h4>校正後</h4>
              <button
                onClick={() => copyToClipboard(correctedText)}
                style={{
                  position: 'absolute',
                  right: 0,
                  top: 0,
                  padding: '0.25rem 0.5rem',
                  fontSize: '12px',
                }}
              >
                コピー
              </button>
              <div style={{ whiteSpace: 'pre-wrap', border: '1px solid #ccc', padding: '1rem' }}>
                {correctedText}
              </div>
            </div>
          </div>
        </div>
      )}

      {/* トースト */}
      {toastMessage && (
        <div
          style={{
            position: 'fixed',
            bottom: 20,
            right: 20,
            background: '#333',
            color: '#fff',
            padding: '0.75rem 1.25rem',
            borderRadius: 6,
            fontSize: 14,
          }}
        >
          {toastMessage}
        </div>
      )}
    </div>
  );
}

export default App;
