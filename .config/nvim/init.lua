-- Line numbers, highlights, etc.
vim.wo.number = true
vim.wo.relativenumber = true
vim.wo.cursorline = true
vim.wo.colorcolumn = '80'

-- Indentations
vim.opt.tabstop = 4
vim.opt.expandtab = true
vim.opt.softtabstop = 4
vim.opt.shiftwidth = 4

-- vsplit opens new pane to the right
vim.opt.splitright = true

-- set leader to be Space
vim.g.mapleader = ' '

-- Yank to clipboard
vim.opt.clipboard = "unnamedplus"

-- Better search settings
vim.opt.ignorecase = true
vim.opt.smartcase = true

-- Better scrolling options
vim.opt.scrolloff = 10 -- keep 10 lines below/above cursor

-- Borders for popup windows
vim.o.winborder = 'rounded'


-- ==============================
-- Keybinds
-- ==============================
vim.keymap.set('n', '<leader>c', ':nohlsearch<CR>', { desc = "Clear search highlights" })

-- ==============================
-- Autocmds
-- ==============================
vim.api.nvim_create_autocmd("TextYankPost", {
  group = augroup,
  callback = function()
    vim.highlight.on_yank()
  end,
})

-- ==============================
-- Packages
-- ==============================
vim.pack.add{
    'https://github.com/neovim/nvim-lspconfig',
    'https://github.com/folke/tokyonight.nvim',
    'https://github.com/mason-org/mason.nvim',
    'https://www.github.com/ibhagwan/fzf-lua',
    -- Snippets
    {
		src = 'https://github.com/saghen/blink.cmp',
		version = vim.version.range("1.*"),
	},
    'https://github.com/rafamadriz/friendly-snippets',

    'https://github.com/nvim-lua/plenary.nvim', -- dependency for none-ls
    'https://github.com/nvimtools/none-ls.nvim',
    'https://github.com/romus204/tree-sitter-manager.nvim',
    'https://github.com/Vigemus/iron.nvim', -- REPLs
    'https://github.com/nvim-tree/nvim-web-devicons',
    'https://github.com/nvim-lualine/lualine.nvim',
    -- Debugging
    'https://codeberg.org/mfussenegger/nvim-dap.git',
    'https://github.com/igorlfs/nvim-dap-view',
    'https://codeberg.org/mfussenegger/nvim-dap-python',
}

-- Set colorscheme, now that it's installed
vim.cmd('colorscheme tokyonight')

-- Initialize lualine
require('lualine').setup()


-- ==============================
-- FZF-lua
-- ==============================
require('fzf-lua').setup({})
-- Keybinds
vim.keymap.set('n', '<leader>ff', function ()
    require('fzf-lua').files()
end, {desc = 'FZF Files'})
vim.keymap.set("n", "<leader>fg", function()
	require("fzf-lua").live_grep()
end, { desc = "FZF Live Grep" })
vim.keymap.set("n", "<leader>fb", function()
	require("fzf-lua").buffers()
end, { desc = "FZF Buffers" })
vim.keymap.set("n", "<leader>fh", function()
	require("fzf-lua").help_tags()
end, { desc = "FZF Help Tags" })
vim.keymap.set("n", "<leader>fx", function()
	require("fzf-lua").diagnostics_document()
end, { desc = "FZF Diagnostics Document" })
vim.keymap.set("n", "<leader>fX", function()
	require("fzf-lua").diagnostics_workspace()
end, { desc = "FZF Diagnostics Workspace" })

-- Mason
require('mason').setup({})

-- ==============================
-- LSP, snippets, etc
-- ==============================

-- Inline diagnostics
vim.diagnostic.config({ virtual_lines = true })

-- Start treesitter with vim API
require("tree-sitter-manager").setup()
-- vim.treesitter.start() -- TODO errors out; determine necessity/cause
vim.api.nvim_create_autocmd('FileType', {
  pattern = {'sh'},
  callback = function()
    vim.treesitter.start()
  end
})

vim.api.nvim_create_autocmd('FileType', {
    pattern = {'lua', 'py'},
    callback = function ()
        vim.treesitter.start()
        vim.treesitter.foldexpr()
    end
})

-- Start LSPs
vim.lsp.enable({'pyright', 'bashls', 'lua_ls', 'r_language_server'})

-- None-ls
require('null-ls').setup({})

-- Blink.cmp
require("blink.cmp").setup({
	keymap = { preset = 'default' },
	appearance = { nerd_font_variant = "mono" },
	sources = { default = { "lsp", "path", "buffer", "snippets" } },
	fuzzy = {
		implementation = "prefer_rust",
		prebuilt_binaries = { download = true },
	},
})

vim.lsp.config['*'] = {
    capabilities = require('blink.cmp').get_lsp_capabilities(),
}

-- ==============================
-- Iron.nvim
-- ==============================
-- Uses mostly the recommended config
local iron = require("iron.core")
local view = require("iron.view")
local common = require("iron.fts.common")

iron.setup {
  config = {
    -- Whether a repl should be discarded or not
    scratch_repl = true,
    -- Your repl definitions come here
    repl_definition = {
      sh = {
        -- Can be a table or a function that
        -- returns a table (see below)
        command = {"zsh"}
      },
      python = {
        command = { "ipython", "--no-autoindent" },
        format = common.bracketed_paste_python,
        block_dividers = { "# %%", "#%%" },
        env = {PYTHON_BASIC_REPL = "1"} --this is needed for python3.13 and up.
      },
      r = {
        command = {"R"}
      }
    },
    -- set the file type of the newly created repl to ft
    -- bufnr is the buffer id of the REPL and ft is the filetype of the 
    -- language being used for the REPL. 
    repl_filetype = function(bufnr, ft)
      return ft
      -- or return a string name such as the following
      -- return "iron"
    end,
    -- Send selections to the DAP repl if an nvim-dap session is running.
    dap_integration = true,
    -- How the repl window will be displayed
    -- See below for more information
    repl_open_cmd = view.bottom(10),

    -- repl_open_cmd can also be an array-style table so that multiple 
    -- repl_open_commands can be given.
    -- When repl_open_cmd is given as a table, the first command given will
    -- be the command that `IronRepl` initially toggles.
    -- Moreover, when repl_open_cmd is a table, each key will automatically
    -- be available as a keymap (see `keymaps` below) with the names 
    -- toggle_repl_with_cmd_1, ..., toggle_repl_with_cmd_k
    -- For example,
    -- 
    -- repl_open_cmd = {
    --   view.split.vertical.rightbelow("%40"), -- cmd_1: open a repl to the right
    --   view.split.rightbelow("%25")  -- cmd_2: open a repl below
    -- }

  },
  -- Iron doesn't set keymaps by default anymore.
  -- You can set them here or manually add keymaps to the functions in iron.core
  keymaps = {
    toggle_repl = "<space>rr", -- toggles the repl open and closed.
    -- If repl_open_command is a table as above, then the following keymaps are
    -- available
    -- toggle_repl_with_cmd_1 = "<space>rv",
    -- toggle_repl_with_cmd_2 = "<space>rh",
    restart_repl = "<space>rR", -- calls `IronRestart` to restart the repl
    send_motion = "<space>sc",
    visual_send = "<space>sc",
    send_file = "<space>sf",
    send_line = "<space>sl",
    send_paragraph = "<space>sp",
    send_until_cursor = "<space>su",
    send_mark = "<space>sm",
    send_code_block = "<space>sb",
    send_code_block_and_move = "<space>sn",
    mark_motion = "<space>mc",
    mark_visual = "<space>mc",
    remove_mark = "<space>md",
    cr = "<space>s<cr>",
    interrupt = "<space>s<space>",
    exit = "<space>sq",
    clear = "<space>cl",
  },
  -- If the highlight is on, you can change how it looks
  -- For the available options, check nvim_set_hl
  highlight = {
    italic = true
  },
  ignore_blank_lines = true, -- ignore blank lines when sending visual select lines
}

-- iron also has a list of commands, see :h iron-commands for all available commands
vim.keymap.set('n', '<space>rf', '<cmd>IronFocus<cr>')
vim.keymap.set('n', '<space>rh', '<cmd>IronHide<cr>')

-- Exit terminal mode with Esc key
vim.keymap.set('t', '<Esc>', [[<C-\><C-n>]])


-- ==============================
-- Debugging
-- ==============================
local dap = require('dap')
require('dap-view')
require('dap-python').setup('python3')

vim.keymap.set('n', '<leader>dt', '<cmd>DapViewToggle<cr>')
vim.keymap.set('n', '<leader>db', dap.toggle_breakpoint, {})
vim.keymap.set('n', '<leader>dc', dap.continue, {})
vim.keymap.set('n', '<leader>dw', '<cmd>DapViewWatch<cr>')
vim.keymap.set('n', '<leader>di', dap.step_into, {})
vim.keymap.set('n', '<leader>do', dap.step_over, {})
vim.keymap.set('n', '<leader>dO', dap.step_out, {})
