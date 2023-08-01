s.boot
// Precussive synth with envelope
(
SynthDef(\klank, {
	arg freq=100, amp=0.1, ring_time=5;
	var n = 10;
	var ratio = [9/8, 5/4, 4/3, 3/2, 5/3, 15/8];
	var beater, sig, trig;
	var env;
	beater = PinkNoise.ar(0.05!2)*Env.perc(0,0.01).kr;
	sig = Klank.ar(`[
		Array.geom(n,freq, ratio.choose),
		Array.exprand(n, 0.2, 0.2),
		Array.exprand(n, ring_time*3, ring_time*3)
	],beater);
	env= EnvGen.kr(Env.new([1,1,0],[20,1]),doneAction:2);
	Out.ar(0, sig*env);

};
).add
)


// Synth without envelope
(
SynthDef(\fm, {
	arg freq=500, mRatio=3, cRatio=3,
	amp=0.2;
	var car, mod;

	mod = SinOsc.ar(freq * mRatio, mul:freq * mRatio);
	car = SinOsc.ar(freq * cRatio + mod) * amp;
	Out.ar(0, car!2);
}).add;
)


// Read the png file and write a scd file to output.scd
// Edit the main.py file to modify paramters or read different input files
(
~out = "cd " + thisProcess.nowExecutingPath.dirname+"; cd .. ; venv/bin/python main.py";
~out.unixCmdGetStdOut
)

// Read the scd. Mainly for debugging
"output.scd".loadRelative();

// Read the scd and play the score.
// Example with Pmono
(
"output.scd".loadRelative();
(
Array.series(~duration_amp.size
).do{|idx|
	Pmono(
		\fm,
		\amp, 5/~duration_amp.size*Pseg(Pseq(~amp[idx]),Pseq(~duration_amp[idx])),
		\freq, Pseg(Pseq(~mean[idx]),Pseq(~duration_amp[idx]))/5,
		\cRatio, Pseg(Pseq(~distance[idx]),Pseq(~duration_amp[idx]))/100,

		\dur, 0.03
).play;
}))


// Read the scd and play the score.
// Example with Pseq for percussive sounds with envelope
(
"output.scd".loadRelative();

Array.series(~duration_amp.size
).do{|idx|
	Pbind(
		\instrument, \klank,
		\freq, Pseq([0,~mean[idx][0]]),
		\dur, Pseq(~duration_single[idx]),
		\amp, 5/ ~duration_amp.size,
		\ring_time, Pseq(~length_single[idx])
).play;
})
