
%---

dataDir = '../data/';
dataIDs = {'m4404ee', 'c6404ee'};

size_dataIDs = size(dataIDs);
for i = 1:size_dataIDs(2)
    fileName = dataIDs{i};
    mat2csv(dataDir, dataIDs{i});
end

function mat2csv(dataDir, dataFileID)

    mkdir([dataDir dataFileID])
    dataOutPrefix = [dataDir dataFileID '/'];
    dataSuffix = '.txt';
    load([dataDir dataFileID '_allunits.mat'])
    outFileHandler = fopen([dataOutPrefix 'Tbhv' dataSuffix],'w');
    format = '%d, %d, %d, %d, %d, %d, %d, %d, %d, %d\n';
    fprintf(outFileHandler, format, Tbhv');

    outFileHandler = fopen([dataOutPrefix 'trTarget' dataSuffix], 'w');
    fprintf(outFileHandler, string('%d\n'), trTarget);

    outFileHandler = fopen([dataOutPrefix 'analogAx' dataSuffix], 'w');
    fprintf(outFileHandler, string('%d\n'), analogAx);

    outFileHandler = fopen([dataOutPrefix 'ANdat' dataSuffix], 'w');
    size_ANdat = size(ANdat);
    format = '';
    for elem = 1:(size_ANdat(2)-1)
       format = [format '%d, '];
    end
    format = [format, '%d\n'];
    fprintf(outFileHandler, format, ANdat);
    %---
    files = who('unit*');
    for uID = 1:size(files,1)
      fileID = files{uID};
      outFileName = [dataOutPrefix fileID dataSuffix];
      outFileHandler = fopen(outFileName, 'w');

      fprintf(outFileHandler, 'Spikes:\n');
      size_Spikes = size(unit101.Spikes);
      format = '';
      for elem = 1:(size_Spikes(2)-1)
        format = [format '%d, '];
      end
      format = [format, '%d\n'];
      eval(makeCommand4component('Spikes''', fileID));

      format = 'IS: %d\n';
      eval(makeCommand4component('IS', fileID));

      format = 'XYZ: %d, %d, %d\n';
      eval(makeCommand4component('XYZ', fileID));

      format = 'Loc: %s\n';
      eval(makeCommand4component('loc', fileID));

      format = 'Stab: ';
      size_Stab = size(unit101.Stab);
      for elem = (1:size_Stab(1)-1)
        format = [format, '%d, '];
      end
      format = [format, '%d\n'];
      eval(makeCommand4component('Stab', fileID));
    end
end

function command = makeCommand4component(component, fileID)
  command = ['fprintf(outFileHandler, format, ' fileID '.' component ');'];
end

%---
