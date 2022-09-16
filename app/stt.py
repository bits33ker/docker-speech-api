import numpy as np
from deepspeech import Model
import av
import logging
from flask import json

class DeepSpeech:
    def init_model(self, model_path, scorer, beam_width, lm_alpha, lm_beta):
        print("creating model {} with scorer {}...".format(model_path, scorer))
        self.model = Model(model_path)

        if scorer is not None:
            self.model.enableExternalScorer(scorer)
            if lm_alpha is not None and lm_beta is not None:
                if self.model.setScorerAlphaBeta(lm_alpha, lm_beta) != 0:
                    raise RuntimeError("Unable to set scorer parameters")

        if beam_width is not None:
            if self.model.setBeamWidth(beam_width) != 0:
                raise RuntimeError("Unable to set beam width")

        print("model is ready.")

    def Recognize(self, audiofile):
            if self.model is None:
                return 'ERROR. No model assign'

            try: 
                text = ''                   
                audio = av.open(audiofile)
                if len(audio.streams.audio) > 1:
                    logging.warning("Audio has more than one stream. Only one of them will be used.")

                #resampler = av.audio.resampler.AudioResampler(
                #    format="s16", layout="mono", rate=16000
                #)
                resampled_frames = []
                for frame in audio.decode(audio=0):
                    resample = frame #resampler.resample(frame)
                    #for r in resample: 
                    resampled_frames.append(resample.to_ndarray().flatten())
                    #resampled_frames.append(np.array(resample).flatten())

                data8 = np.concatenate(resampled_frames, dtype=np.int16)
                # audio = decoding.decode_audio(io.BytesIO(data))
                transcript = self.model.sttWithMetadata(data8)#stt
                confidence = transcript.transcripts[0].confidence
                text = ''
                for t in transcript.transcripts[0].tokens:
                    text = text + t.text
                
                print("STT result: {}".format(text))
            except Exception as e:
                print("STT error: {}".format(e))

            r = json.dumps({'results': [{'text': text, 'confidence': confidence}]})
            return json.loads(r)