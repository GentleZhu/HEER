INPUTDIR = ./input_data
INTMEDIR = ./intermediate_data
MODELDIR = ./intermediate_data/model
PERTYPEDIR = ./intermediate_data/per_type_temp
OUTPUTDIR = ./output
LOGDIR = ./log

all: 
	mkdir -p $(INPUTDIR) $(INTMEDIR) $(MODELDIR) $(PERTYPEDIR) $(OUTPUTDIR) $(LOGDIR)

# intentionally omitted make clean to avoid accidentally deleting all data
