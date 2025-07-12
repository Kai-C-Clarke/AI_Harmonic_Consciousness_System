import { useState } from 'react';
import { Card } from '@/components/ui/card';
import { Badge } from '@/components/ui/badge';
import YamlEditor from '@/components/YamlEditor';
import MidiPreview from '@/components/MidiPreview';

const Index = () => {
  const [yamlContent, setYamlContent] = useState('');
  const [parsedData, setParsedData] = useState<any>(null);

  return (
    <div className="min-h-screen bg-background">
      {/* Header */}
      <header className="border-b border-border bg-card/50 backdrop-blur">
        <div className="container mx-auto px-4 py-6">
          <div className="flex items-center justify-between">
            <div>
              <h1 className="text-3xl font-bold bg-gradient-to-r from-studio-gradient1 to-studio-gradient2 bg-clip-text text-transparent">
                Melody Scribe
              </h1>
              <p className="text-muted-foreground mt-1">Convert YAML to MIDI with ease</p>
            </div>
            <div className="flex items-center gap-2">
              <Badge variant="outline" className="text-waveform border-waveform/30">
                YAML → MIDI
              </Badge>
            </div>
          </div>
        </div>
      </header>

      {/* Main Content */}
      <main className="container mx-auto px-4 py-8">
        <div className="grid lg:grid-cols-2 gap-8">
          {/* YAML Editor */}
          <div>
            <YamlEditor
              value={yamlContent}
              onChange={setYamlContent}
              onValidYaml={setParsedData}
            />
          </div>

          {/* MIDI Preview */}
          <div>
            <MidiPreview data={parsedData} />
          </div>
        </div>

        {/* Instructions */}
        <Card className="mt-8 p-6 bg-gradient-to-br from-card to-secondary/30">
          <h3 className="text-lg font-semibold mb-4 text-studio-purple">How to Use</h3>
          <div className="grid md:grid-cols-3 gap-4 text-sm">
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-studio-gradient1 text-primary-foreground flex items-center justify-center text-xs font-bold">
                1
              </div>
              <div>
                <p className="font-medium">Write or paste YAML</p>
                <p className="text-muted-foreground">Define your musical structure in YAML format</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-studio-gradient2 text-primary-foreground flex items-center justify-center text-xs font-bold">
                2
              </div>
              <div>
                <p className="font-medium">Preview structure</p>
                <p className="text-muted-foreground">See your musical data organized and validated</p>
              </div>
            </div>
            <div className="flex items-start gap-3">
              <div className="w-6 h-6 rounded-full bg-waveform text-primary-foreground flex items-center justify-center text-xs font-bold">
                3
              </div>
              <div>
                <p className="font-medium">Generate MIDI</p>
                <p className="text-muted-foreground">Convert to standard MIDI file format</p>
              </div>
            </div>
          </div>
        </Card>
      </main>
    </div>
  );
};

export default Index;
