"""
User Interface Management Layer.
Modern Dashboard Design.
"""
import pygame
import utils.config as cfg

class ModernButton:
    def __init__(self, x, y, width, height, text, action_payload):
        self.rect = pygame.Rect(x, y, width, height)
        self.text = text
        self.action_payload = action_payload
        
        self.col_idle = cfg.COLOR_PANEL
        self.col_hover = cfg.COLOR_FRONTIER
        self.col_active = cfg.COLOR_PATH
        self.col_text = cfg.COLOR_TEXT_MAIN
        
        self.font = pygame.font.SysFont("JetBrainsMono Nerd Font", 16, bold=True)
        self.active = False

    def draw(self, surface, is_selected=False):
        mouse_pos = pygame.mouse.get_pos()
        is_hovered = self.rect.collidepoint(mouse_pos)
        
        if is_selected:
            bg_color = self.col_active
            text_color = cfg.COLOR_SIDEBAR
        elif is_hovered:
            bg_color = self.col_hover
            text_color = cfg.COLOR_SIDEBAR
        else:
            bg_color = self.col_idle
            text_color = self.col_text

        pygame.draw.rect(surface, bg_color, self.rect, border_radius=8)
        
        text_surf = self.font.render(self.text, True, text_color)
        text_rect = text_surf.get_rect(center=self.rect.center)
        surface.blit(text_surf, text_rect)

    def is_clicked(self, pos):
        return self.rect.collidepoint(pos)


class InterfaceRenderer:
    def __init__(self, display_surface):
        self.display = display_surface
        
        self.font_title = pygame.font.SysFont("JetBrainsMono Nerd Font", 28, bold=True)
        self.font_label = pygame.font.SysFont("JetBrainsMono Nerd Font", 14)
        self.font_value = pygame.font.SysFont("JetBrainsMono Nerd Font", 20, bold=True)
        
        self.sidebar_width = 280
        self.padding = 20
        
        self.buttons = []
        algos = ["BFS", "DFS", "UCS", "DLS", "IDDFS", "BIDIRECTIONAL"]
        
        btn_start_y = 280
        btn_height = 40
        for i, algo in enumerate(algos):
            y_pos = btn_start_y + (i * (btn_height + 10))
            btn = ModernButton(
                self.padding, 
                y_pos, 
                self.sidebar_width - (self.padding * 2), 
                btn_height, 
                algo, 
                algo
            )
            self.buttons.append(btn)

    def render_control_panel(self, active_algorithm, status):
        sidebar_rect = pygame.Rect(0, 0, self.sidebar_width, cfg.WINDOW_HEIGHT)
        pygame.draw.rect(self.display, cfg.COLOR_SIDEBAR, sidebar_rect)
        
        title_surf = self.font_title.render("PATHFINDER", True, cfg.COLOR_PATH)
        self.display.blit(title_surf, (self.padding, 30))
        
        sub_surf = self.font_label.render("AI VISUALIZER v2.0", True, cfg.COLOR_GRID)
        self.display.blit(sub_surf, (self.padding, 65))

        panel_rect = pygame.Rect(self.padding, 110, self.sidebar_width - 40, 140)
        pygame.draw.rect(self.display, cfg.COLOR_PANEL, panel_rect, border_radius=12)
        
        lbl_status = self.font_label.render("CURRENT STATUS", True, cfg.COLOR_FRONTIER)
        self.display.blit(lbl_status, (panel_rect.x + 15, panel_rect.y + 15))
        
        col_status = cfg.COLOR_START if status == "FINISHED" else (cfg.COLOR_TARGET if status == "RUNNING" else cfg.COLOR_TEXT_MAIN)
        val_status = self.font_value.render(status, True, col_status)
        self.display.blit(val_status, (panel_rect.x + 15, panel_rect.y + 35))

        pygame.draw.line(self.display, cfg.COLOR_SIDEBAR, (panel_rect.x + 10, panel_rect.y + 70), (panel_rect.right - 10, panel_rect.y + 70), 2)

        lbl_algo = self.font_label.render("SELECTED ALGORITHM", True, cfg.COLOR_FRONTIER)
        self.display.blit(lbl_algo, (panel_rect.x + 15, panel_rect.y + 85))
        
        val_algo = self.font_value.render(active_algorithm, True, cfg.COLOR_TEXT_MAIN)
        self.display.blit(val_algo, (panel_rect.x + 15, panel_rect.y + 105))

        for btn in self.buttons:
            is_selected = (btn.action_payload == active_algorithm)
            btn.draw(self.display, is_selected)

        instr_y = cfg.WINDOW_HEIGHT - 120
        keys = [
            ("SPACE", "Start Search"),
            ("C", "Clear Grid"),
            ("L-CLICK", "Place Node"),
            ("R-CLICK", "Remove Node")
        ]
        
        for key, desc in keys:
            k_surf = self.font_label.render(f"[{key}]", True, cfg.COLOR_FRONTIER)
            d_surf = self.font_label.render(desc, True, cfg.COLOR_GRID)
            
            self.display.blit(k_surf, (self.padding, instr_y))
            self.display.blit(d_surf, (self.padding + 80, instr_y))
            instr_y += 22

    def render_result_popup(self, success, duration):
        dim_surf = pygame.Surface((cfg.WINDOW_WIDTH, cfg.WINDOW_HEIGHT), pygame.SRCALPHA)
        dim_surf.fill((0, 0, 0, 150))
        self.display.blit(dim_surf, (0, 0))

        cw, ch = 400, 250
        cx = (cfg.WINDOW_WIDTH // 2) - (cw // 2)
        cy = (cfg.WINDOW_HEIGHT // 2) - (ch // 2)
        
        modal_rect = pygame.Rect(cx, cy, cw, ch)
        
        pygame.draw.rect(self.display, cfg.COLOR_SIDEBAR, modal_rect, border_radius=15)
        pygame.draw.rect(self.display, cfg.COLOR_PANEL, modal_rect, 2, border_radius=15)

        header_text = "SEARCH COMPLETE"
        sub_text = "Target Found Successfully" if success else "Target Unreachable"
        color = cfg.COLOR_START if success else cfg.COLOR_TARGET
        
        surf_header = self.font_value.render(header_text, True, cfg.COLOR_TEXT_MAIN)
        surf_sub = self.font_label.render(sub_text, True, color)
        
        self.display.blit(surf_header, (cx + 30, cy + 30))
        self.display.blit(surf_sub, (cx + 30, cy + 60))

        stats_rect = pygame.Rect(cx + 30, cy + 100, cw - 60, 60)
        pygame.draw.rect(self.display, cfg.COLOR_PANEL, stats_rect, border_radius=8)
        
        time_lbl = self.font_label.render("Time Elapsed:", True, cfg.COLOR_GRID)
        time_val = self.font_value.render(f"{duration:.4f}s", True, cfg.COLOR_TEXT_MAIN)
        
        self.display.blit(time_lbl, (stats_rect.x + 15, stats_rect.y + 10))
        self.display.blit(time_val, (stats_rect.x + 15, stats_rect.y + 30))

        footer = self.font_label.render("Press 'C' to Reset Grid", True, cfg.COLOR_FRONTIER)
        footer_rect = footer.get_rect(center=(cx + cw//2, cy + ch - 30))
        self.display.blit(footer, footer_rect)

    def check_button_clicks(self, pos):
        for btn in self.buttons:
            if btn.is_clicked(pos):
                return btn.action_payload
        return None
