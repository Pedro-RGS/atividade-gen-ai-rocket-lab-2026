import { useState, type FormEvent } from "react";
import { CustomInput } from "../atoms/custom-input";
import { CustomIcon } from "../atoms/custom-icon";
import { CustomButton } from "../atoms/custom-button"
import { Search } from "lucide-react";

interface SearchBarProps {
  onSearch: (value: string) => void;
  placeholder?: string;
}

export const SearchBar = ({
  onSearch,
  placeholder
}: SearchBarProps) => { 
  const [searchValue, setSearchValue] = useState('')
  
  const handleSubmit = (e: FormEvent<HTMLFormElement>) => {
    e.preventDefault();
    onSearch(searchValue);
  }

  return (
    <form
      onSubmit={handleSubmit}
      className="flex items-center gap-2 w-full max-w-2xl"
    >
      <div className="relative flex-1">
        <div className="absolute left-3 top-1/2 -translate-y-1/2 z-10 pointer-events-none">
          <CustomIcon icon={Search} size="md" className="text-zinc-500" />
        </div>
        <CustomInput
          placeholder={placeholder}
          value={searchValue}
          onChange={(e) => setSearchValue(e.target.value)}
          className="pl-10 bg-zinc-900 border-zinc-800 text-white focus:border-yellow-500"
        />
      </div>
      <CustomButton
        type="submit"
        variant="primary"
        className="rounded-none uppercase italic font-black"
      >
        Buscar
      </CustomButton>
    </form>
  );
}