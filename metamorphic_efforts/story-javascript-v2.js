// ============================================================
// METAMORPHIC EFFORTS - Story JavaScript
// Hybrid architecture. Twine = interface. TouchDesigner = headless visuals.
// Bidirectional WebSocket.
// Five polyphonic audio layers.
// LMA annotation with progressive reveal and toggle.
// ============================================================

window.ME = window.ME || {};
ME.wsUrl = 'ws://localhost:9980';
ME.ws = null;
ME.totalPassages = 10;
ME.currentBess = null;
ME.targetBess = null;
ME.lmaVisible = true;
ME.revealDelay = 8000;
ME.autoTimer = null;
ME.revealTimer = null;
ME.nextPassageTarget = null;
ME.layerTimers = [];

// ============================================================
// AUDIO MAPS
// ============================================================

ME.DRONE_MAP = {
  'press_low':  'audio/drones/drone_press_low.mp3',
  'press_high': 'audio/drones/drone_press_high.mp3',
  'wring':      'audio/drones/drone_wring.mp3',
  'glide':      'audio/drones/drone_glide.mp3',
  'slash':      'audio/drones/drone_slash.mp3'
};

ME.DRONE_PASSAGE = {
  1: 'press_low',  2: 'press_low',  3: 'press_low',
  4: 'press_high', 5: 'wring',      6: 'press_high',
  7: 'wring',      8: 'glide',      9: 'slash',
  10: 'slash'
};

ME.SFX_MAP = {
  1:  ['audio/sfx/sfx_room_ambience.mp3', 'audio/sfx/sfx_body_rustle.mp3'],
  2:  ['audio/sfx/sfx_rain_window.mp3', 'audio/sfx/sfx_clock_ticking.mp3'],
  3:  ['audio/sfx/sfx_body_thrashing.mp3', 'audio/sfx/sfx_insect_legs.mp3'],
  4:  ['audio/sfx/sfx_clock_ticking.mp3'],
  5:  [],
  6:  ['audio/sfx/sfx_body_thrashing.mp3', 'audio/sfx/sfx_insect_legs.mp3'],
  7:  [],
  8:  ['audio/sfx/sfx_key_turning.mp3', 'audio/sfx/sfx_fluid_drip.mp3'],
  9:  ['audio/sfx/sfx_door_open.mp3', 'audio/sfx/sfx_gasp.mp3', 'audio/sfx/sfx_body_thud.mp3'],
  10: ['audio/sfx/sfx_newspaper_swat.mp3', 'audio/sfx/sfx_body_scrape.mp3', 'audio/sfx/sfx_door_slam.mp3']
};

ME.CHAR_MAP = {
  1: [], 2: [], 3: [],
  4:  ['audio/characters/char_knock_door.mp3', 'audio/characters/char_mother_call.mp3'],
  5:  [], 6: [],
  7:  ['audio/characters/char_knock_loud.mp3', 'audio/characters/char_manager_footsteps.mp3', 'audio/characters/char_grete_cry.mp3'],
  8:  [],
  9:  ['audio/characters/char_grete_cry.mp3'],
  10: ['audio/characters/char_father_hissing.mp3', 'audio/characters/char_father_pacing.mp3', 'audio/characters/char_door_slam.mp3']
};

ME.PASSAGE_MIX = {
  1:  { narration: 0.9,  body_vox: 0.3,  drone: 0.4,  sfx: 0.3,  characters: 0.0 },
  2:  { narration: 0.9,  body_vox: 0.25, drone: 0.45, sfx: 0.35, characters: 0.0 },
  3:  { narration: 0.85, body_vox: 0.35, drone: 0.5,  sfx: 0.35, characters: 0.0 },
  4:  { narration: 0.85, body_vox: 0.35, drone: 0.55, sfx: 0.4,  characters: 0.4 },
  5:  { narration: 0.8,  body_vox: 0.4,  drone: 0.6,  sfx: 0.3,  characters: 0.0 },
  6:  { narration: 0.8,  body_vox: 0.45, drone: 0.55, sfx: 0.45, characters: 0.0 },
  7:  { narration: 0.75, body_vox: 0.4,  drone: 0.6,  sfx: 0.35, characters: 0.6 },
  8:  { narration: 0.9,  body_vox: 0.3,  drone: 0.5,  sfx: 0.4,  characters: 0.0 },
  9:  { narration: 0.7,  body_vox: 0.45, drone: 0.65, sfx: 0.5,  characters: 0.5 },
  10: { narration: 0.8,  body_vox: 0.0,  drone: 0.7,  sfx: 0.6,  characters: 0.7 }
};

// ============================================================
// WEBSOCKET
// ============================================================

ME.connectWS = function() {
  try {
    ME.ws = new WebSocket(ME.wsUrl);
    ME.ws.binaryType = 'arraybuffer';

    ME.ws.onopen = function() {
      var d = document.getElementById('me-dot');
      var l = document.getElementById('me-label');
      if (d) d.className = 'connected';
      if (l) l.textContent = 'td connected';
      console.info('ME: WebSocket connected to', ME.wsUrl);
    };

    ME.ws.onmessage = function(e) {
      var label = document.getElementById('me-label');
      if (e.data instanceof ArrayBuffer || e.data instanceof Blob) {
        if (label) label.textContent = 'td frame';
        ME.drawTDFrame(e.data);
      } else if (typeof e.data === 'string') {
        var src = null;
        if (e.data.indexOf('data:image/') === 0) {
          src = e.data;
        } else if (/^[A-Za-z0-9+/=\s]+$/.test(e.data) && e.data.length > 100) {
          src = 'data:image/jpeg;base64,' + e.data.replace(/\s+/g, '');
        } else {
          try {
            var json = JSON.parse(e.data);
            if (json && typeof json.data === 'string') {
              if (json.data.indexOf('data:image/') === 0) {
                src = json.data;
              } else {
                var mime = json.type || 'image/jpeg';
                src = 'data:' + mime + ';base64,' + json.data.replace(/\s+/g, '');
              }
            }
          } catch (err) {}
        }
        if (src) {
          if (label) label.textContent = 'td frame';
          ME.drawTDFrameDataURL(src);
        }
      }
    };

    ME.ws.onclose = function() {
      var d = document.getElementById('me-dot');
      var l = document.getElementById('me-label');
      if (d) d.className = 'fallback';
      if (l) l.textContent = 'disconnected';
      setTimeout(ME.connectWS, 4000);
    };

    ME.ws.onerror = function(err) {
      console.warn('ME: WS error', err);
    };
  } catch (e) {
    console.warn('ME: WS connection failed', e);
  }
};

ME.sendBESS = function(data) {
  if (ME.ws && ME.ws.readyState === WebSocket.OPEN) {
    ME.ws.send(JSON.stringify(data));
  }
};

// ============================================================
// CANVAS
// ============================================================

ME.initCanvas = function() {
  ME.canvas = document.getElementById('me-canvas');
  ME.canvas.width = 854;
  ME.canvas.height = 480;
  ME.ctx = ME.canvas.getContext('2d');
  ME.frameImg = new Image();
};

ME.drawTDFrame = function(buf) {
  if (!buf) return;
  var blob = buf instanceof Blob ? buf : new Blob([buf], { type: 'image/jpeg' });
  var url = URL.createObjectURL(blob);
  ME.frameImg.onload = function() {
    if (!ME.ctx) return;
    ME.ctx.drawImage(ME.frameImg, 0, 0, 854, 480);
    URL.revokeObjectURL(url);
  };
  ME.frameImg.onerror = function(err) {
    console.warn('ME: TD frame failed to load', err);
    URL.revokeObjectURL(url);
  };
  ME.frameImg.src = url;
};

ME.drawTDFrameDataURL = function(dataURL) {
  if (!dataURL) return;
  ME.frameImg.onload = function() {
    if (!ME.ctx) return;
    ME.ctx.drawImage(ME.frameImg, 0, 0, 854, 480);
  };
  ME.frameImg.onerror = function(err) {
    console.warn('ME: TD frame data URL failed', err);
  };
  ME.frameImg.src = dataURL;
};

// ============================================================
// WEB AUDIO API
// ============================================================

ME.audioCtx = null;
ME.layers = {};

ME.initAudio = function() {
  ME.audioCtx = new (window.AudioContext || window.webkitAudioContext)();
  ME.masterGain = ME.audioCtx.createGain();
  ME.masterGain.gain.value = 1.0;
  ME.masterGain.connect(ME.audioCtx.destination);

  var defs = [
    { id: 'narration',  g: 0.9,  l: 'Narration' },
    { id: 'body_vox',   g: 0.35, l: 'Body' },
    { id: 'drone',      g: 0.7,  l: 'Drone' },
    { id: 'sfx',        g: 0.4,  l: 'SFX' },
    { id: 'characters', g: 0.5,  l: 'Characters' }
  ];

  defs.forEach(function(d) {
    var gain = ME.audioCtx.createGain();
    gain.gain.value = d.g;
    gain.connect(ME.masterGain);
    ME.layers[d.id] = {
      gain: gain,
      defaultGain: d.g,
      label: d.l,
      sources: []
    };
  });
};

ME.playLayer = function(id, path, opts) {
  opts = opts || {};
  var layer = ME.layers[id];
  if (!layer) return null;

  var audio = new Audio(path);
  audio.loop = opts.loop || false;

  try {
    var source = ME.audioCtx.createMediaElementSource(audio);
    source.connect(layer.gain);
  } catch (e) {
    console.warn('ME: could not connect audio', path);
  }

  if (opts.delay) {
    setTimeout(function() {
      audio.play().catch(function() {});
    }, opts.delay);
  } else {
    audio.play().catch(function() {});
  }

  layer.sources.push(audio);
  return audio;
};

ME.fireSound = function(id, path) {
  var layer = ME.layers[id];
  if (!layer) return;
  var audio = new Audio(path);
  try {
    var source = ME.audioCtx.createMediaElementSource(audio);
    source.connect(layer.gain);
  } catch (e) {}
  audio.play().catch(function() {});
};

ME.stopLayer = function(id) {
  var layer = ME.layers[id];
  if (!layer) return;
  layer.sources.forEach(function(a) {
    try { a.pause(); a.currentTime = 0; } catch (e) {}
  });
  layer.sources = [];
};

ME.setLayerGain = function(id, v) {
  var layer = ME.layers[id];
  if (layer) layer.gain.gain.value = v;
};

// Preload audio, read duration, schedule to end with narration
ME.scheduleLayerToEnd = function(layerId, path, narrDurSec, offsetBefore) {
  offsetBefore = offsetBefore || 0;
  var probe = new Audio(path);

  probe.addEventListener('loadedmetadata', function() {
    var fileDur = probe.duration;
    if (!fileDur || fileDur <= 0) return;

    var startSec = Math.max(2, narrDurSec - fileDur - offsetBefore);
    var startMs = startSec * 1000;

    console.log('ME: ' + layerId + ' (' + path.split('/').pop() + ') dur ' +
      fileDur.toFixed(1) + 's, starting at ' + startSec.toFixed(1) + 's');

    var timer = setTimeout(function() {
      ME.fireSound(layerId, path);
    }, startMs);

    ME.layerTimers.push(timer);
  });

  probe.addEventListener('error', function() {});
  probe.load();
};

// Fade drone out over durationMs
ME.fadeDrone = function(durationMs) {
  var layer = ME.layers['drone'];
  if (!layer) return;
  var startGain = layer.gain.gain.value;
  var steps = 20;
  var stepMs = durationMs / steps;
  var stepVal = startGain / steps;
  var fadeInterval = setInterval(function() {
    var current = layer.gain.gain.value;
    if (current > stepVal) {
      layer.gain.gain.value = current - stepVal;
    } else {
      layer.gain.gain.value = 0;
      clearInterval(fadeInterval);
    }
  }, stepMs);
};

// ============================================================
// AUTO-ADVANCE
// ============================================================

ME.setAutoAdvance = function(target) {
  ME.nextPassageTarget = target;
};

// ============================================================
// LMA ANNOTATION
// ============================================================

ME.revealLMA = function() {
  if (ME.revealTimer) clearTimeout(ME.revealTimer);
  ME.revealTimer = setTimeout(function() {
    if (!ME.lmaVisible) return;
    var spans = document.querySelectorAll('.lma');
    spans.forEach(function(span, i) {
      setTimeout(function() {
        span.classList.add('revealed');
      }, i * 120);
    });
  }, ME.revealDelay);
};

ME.hideLMA = function() {
  document.querySelectorAll('.lma').forEach(function(s) {
    s.classList.remove('revealed');
    s.classList.add('lma-hidden');
  });
};

ME.showLMA = function() {
  document.querySelectorAll('.lma').forEach(function(s) {
    s.classList.remove('lma-hidden');
  });
  ME.revealLMA();
};

ME.toggleLMA = function() {
  ME.lmaVisible = !ME.lmaVisible;
  var dot = document.getElementById('me-lma-toggle-dot');
  var legend = document.getElementById('me-lma-legend');
  if (ME.lmaVisible) {
    if (dot) dot.classList.add('active');
    if (legend) legend.classList.add('visible');
    ME.showLMA();
  } else {
    if (dot) dot.classList.remove('active');
    if (legend) legend.classList.remove('visible');
    ME.hideLMA();
  }
};

// ============================================================
// PASSAGE TRIGGER
// ============================================================

ME.triggerPassage = function(pid, bessData) {
  // Update BESS
  ME.targetBess = bessData;
  if (!ME.currentBess) ME.currentBess = Object.assign({}, bessData);

  // Send to TD
  ME.sendBESS(bessData);

  // Resume AudioContext on first interaction
  if (ME.audioCtx && ME.audioCtx.state === 'suspended') {
    ME.audioCtx.resume();
  }

  // Update UI
  var dn = document.getElementById('me-drive-name');
  if (dn) dn.textContent = bessData.action_drive || '';

  var ctr = document.getElementById('me-counter');
  if (ctr) ctr.textContent = pid > 0 ? pid + ' / 10' : '';

  var prog = document.getElementById('me-progress');
  if (prog) prog.style.width = (pid / 10 * 100) + '%';

  // Apply default mix
  var mix = ME.PASSAGE_MIX[pid];
  if (mix) {
    Object.keys(mix).forEach(function(id) {
      ME.setLayerGain(id, mix[id]);
      var sl = document.getElementById('me-slider-' + id);
      if (sl) sl.value = mix[id] * 100;
    });
  }

  // Stop everything from previous passage
  ME.stopLayer('narration');
  ME.stopLayer('body_vox');
  ME.stopLayer('sfx');
  ME.stopLayer('characters');
  ME.stopLayer('drone');
  if (ME.autoTimer) clearTimeout(ME.autoTimer);
  ME.nextPassageTarget = null;

  if (ME.layerTimers) {
    ME.layerTimers.forEach(function(t) { clearTimeout(t); });
  }
  ME.layerTimers = [];

  if (pid < 1 || pid > 10) {
    ME.revealLMA();
    return;
  }

  // Narration starts immediately
  var narrAudio = ME.playLayer('narration',
    'audio/narration/narr_p' + String(pid).padStart(2, '0') + '.mp3'
  );

  // Once narration duration is known, schedule everything else
  if (narrAudio) {
    narrAudio.addEventListener('loadedmetadata', function() {
      var narrDur = narrAudio.duration;
      if (!narrDur || narrDur <= 0) return;

      console.log('ME: p' + pid + ' narration duration ' + narrDur.toFixed(1) + 's');

      // Auto-advance: narration duration + 3s buffer
      if (ME.nextPassageTarget) {
        var advanceMs = (narrDur * 1000) + 3000;
        if (ME.autoTimer) clearTimeout(ME.autoTimer);

        // Fade drone 2s before advance
        ME.layerTimers.push(setTimeout(function() {
          ME.fadeDrone(2000);
        }, advanceMs - 2000));

        ME.autoTimer = setTimeout(function() {
          Engine.play(ME.nextPassageTarget);
        }, advanceMs);
      }

      // Body vox: schedule to end with narration
      if (pid <= 9) {
        var bvPath = 'audio/body_vox/body_vox_p' + String(pid).padStart(2, '0') + '.mp3';
        ME.scheduleLayerToEnd('body_vox', bvPath, narrDur);
      }

      // SFX: schedule to end with narration
      var sfxFiles = ME.SFX_MAP[pid] || [];
      sfxFiles.forEach(function(f, idx) {
        ME.scheduleLayerToEnd('sfx', f, narrDur, idx * 0.5);
      });

      // Characters: schedule to end with narration
      var charFiles = ME.CHAR_MAP[pid] || [];
      charFiles.forEach(function(f, idx) {
        ME.scheduleLayerToEnd('characters', f, narrDur, idx * 0.3);
      });
    });
  }

  // Drone starts immediately (loops, fades at end)
  var dk = ME.DRONE_PASSAGE[pid];
  if (dk) {
    ME.playLayer('drone', ME.DRONE_MAP[dk], { loop: true });
  }

  // LMA reveal
  ME.revealLMA();
};

// ============================================================
// BESS INTERPOLATION
// ============================================================

ME.lerpBess = function() {
  if (!ME.currentBess || !ME.targetBess) return;
  var keys = [
    'flow', 'intensity', 'weight_passive',
    'shape_grow', 'shape_rise', 'shape_advance',
    'body_connectivity', 'body_sequencing',
    'kinesphere', 'space_approach', 'space_plane'
  ];
  keys.forEach(function(k) {
    if (ME.targetBess[k] !== undefined && ME.currentBess[k] !== undefined) {
      ME.currentBess[k] += (ME.targetBess[k] - ME.currentBess[k]) * 0.02;
    }
  });
};

// ============================================================
// ANIMATION LOOP
// ============================================================

ME.animate = function() {
  ME.lerpBess();
  requestAnimationFrame(ME.animate);
};

// ============================================================
// BUILD UI CONTROLS
// ============================================================

ME.buildControls = function() {
  var ctr = document.getElementById('me-controls');
  if (!ctr) return;

  // Voice sliders
  Object.keys(ME.layers).forEach(function(id) {
    var layer = ME.layers[id];
    var row = document.createElement('div');
    row.className = 'me-slider-row';

    var lbl = document.createElement('label');
    lbl.textContent = layer.label;
    lbl.setAttribute('for', 'me-slider-' + id);

    var sl = document.createElement('input');
    sl.type = 'range';
    sl.id = 'me-slider-' + id;
    sl.min = '0';
    sl.max = '100';
    sl.value = String(layer.defaultGain * 100);
    sl.addEventListener('input', function() {
      ME.setLayerGain(id, this.value / 100);
    });

    row.appendChild(lbl);
    row.appendChild(sl);
    ctr.appendChild(row);
  });

  // Divider
  var div = document.createElement('div');
  div.className = 'me-controls-divider';
  ctr.appendChild(div);

  // LMA annotation toggle
  var toggle = document.createElement('div');
  toggle.id = 'me-lma-toggle';
  toggle.innerHTML = '<label>LMA Annotation</label><div id="me-lma-toggle-dot" class="active"></div>';
  toggle.addEventListener('click', ME.toggleLMA);
  ctr.appendChild(toggle);

  // BESS category legend
  var legend = document.createElement('div');
  legend.id = 'me-lma-legend';
  legend.className = 'visible';
  legend.innerHTML =
    '<span class="me-legend-item"><span class="me-legend-dot effort"></span>Effort</span>' +
    '<span class="me-legend-item"><span class="me-legend-dot shape"></span>Shape</span>' +
    '<span class="me-legend-item"><span class="me-legend-dot body"></span>Body</span>' +
    '<span class="me-legend-item"><span class="me-legend-dot space"></span>Space</span>';
  ctr.appendChild(legend);
};

// ============================================================
// CLEANUP ON PASSAGE CHANGE
// ============================================================

$(document).on(':passageinit', function() {
  if (ME.autoTimer) clearTimeout(ME.autoTimer);
  if (ME.revealTimer) clearTimeout(ME.revealTimer);
  ME.nextPassageTarget = null;
});

// ============================================================
// INITIALIZATION
// ============================================================

$(document).one(':storyready', function() {
  var body = document.body;

  // Canvas
  var canvas = document.createElement('canvas');
  canvas.id = 'me-canvas';
  body.insertBefore(canvas, body.firstChild);

  // Vignette
  var vig = document.createElement('div');
  vig.id = 'me-vignette';
  body.insertBefore(vig, body.children[1]);

  // Drive indicator
  var drv = document.createElement('div');
  drv.id = 'me-drive';
  drv.innerHTML = '<span id="me-drive-name">--</span><span id="me-drive-emotion"></span>';
  body.appendChild(drv);

  // Connection status
  var st = document.createElement('div');
  st.id = 'me-status';
  st.innerHTML = '<span id="me-dot"></span><span id="me-label">connecting</span>';
  body.appendChild(st);

  // Passage counter
  var ct = document.createElement('div');
  ct.id = 'me-counter';
  body.appendChild(ct);

  // Progress bar
  var pb = document.createElement('div');
  pb.id = 'me-progress';
  pb.style.width = '0%';
  body.appendChild(pb);

  // Controls panel
  var cp = document.createElement('div');
  cp.id = 'me-controls';
  cp.innerHTML = '<div id="me-controls-label">Voices</div>';
  body.appendChild(cp);

  // Initialize everything
  ME.initCanvas();
  ME.initAudio();
  ME.buildControls();
  ME.connectWS();
  ME.animate();
});