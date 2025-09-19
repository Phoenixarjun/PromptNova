import { Info } from "lucide-react";
import { Button } from "@/components/ui/button";
import {
  Popover,
  PopoverContent,
  PopoverTrigger,
} from "@/components/ui/popover";
import { Input } from "@/components/ui/input";
import { Label } from "@/components/ui/label";

export function ApiKeyInput() {
  return (
    <div className="grid gap-2">
      <div className="flex items-center justify-between">
        <Label htmlFor="gemini-api-key">Gemini API Key</Label>
        <Popover>
          <PopoverTrigger asChild>
            <Button variant="ghost" size="icon" className="h-6 w-6">
              <Info className="h-4 w-4" />
              <span className="sr-only">API Key Instructions</span>
            </Button>
          </PopoverTrigger>
          <PopoverContent className="w-80" side="top">
            <div className="flex flex-col space-y-2 text-sm">
              <h4 className="font-semibold">How to get your Gemini API Key</h4>
              <ol className="list-decimal list-inside space-y-1">
                <li>
                  Go to{" "}
                  <a
                    href="https://aistudio.google.com/app/apikey"
                    target="_blank"
                    rel="noopener noreferrer"
                    className="text-blue-500 hover:underline"
                  >
                    Google AI Studio
                  </a>
                  .
                </li>
                <li>
                  Click on <strong>"Get API key"</strong>.
                </li>
                <li>
                  Click on <strong>"Create API key in new project"</strong>.
                </li>
                <li>Copy the generated API key and paste it here.</li>
              </ol>
            </div>
          </PopoverContent>
        </Popover>
      </div>
      <Input
        id="gemini-api-key"
        type="password"
        placeholder="Enter your Gemini API key"
      />
    </div>
  );
}