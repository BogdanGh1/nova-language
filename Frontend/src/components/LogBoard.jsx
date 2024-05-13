import React from "react";
import AceEditor from "react-ace";

import "ace-builds/src-noconflict/mode-javascript";
import "ace-builds/src-noconflict/theme-github";
import "ace-builds/src-noconflict/theme-monokai";

function LogBoard({ logs, width,  height }) {
  return (
    <AceEditor
      mode="javascript"
      theme="monokai"
      name="1234"
      fontSize={18}
      width={width}
      height={height}
      value={logs}
      editorProps={{ $blockScrolling: true }}
      readOnly={true}
    />
  );
}

export default LogBoard;
